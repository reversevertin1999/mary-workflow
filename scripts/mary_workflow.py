#!/usr/bin/env python3
"""Tiny runtime helper for Mary Workflow.

This script intentionally avoids third-party dependencies. It writes a simple
YAML-shaped state file and parses only the fields it owns.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path
import re
import sys


WORKFLOW_DIR = ".mary-workflow"
PROMPTS_DIR = "prompts"


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def workflow_root(cwd: Path) -> Path:
    return cwd / WORKFLOW_DIR


def prompt_files(root: Path) -> list[str]:
    prompts = root / PROMPTS_DIR
    if not prompts.exists():
        return []
    return sorted(path.name for path in prompts.iterdir() if path.is_file() and path.suffix == ".md")


def default_state(status: str = "idle") -> dict[str, str | int]:
    return {
        "status": status,
        "started_at": "",
        "updated_at": now_iso(),
        "current_index": 0,
        "current_prompt": "",
        "completed": 0,
        "total": 0,
    }


def read_state(root: Path) -> dict[str, str | int]:
    state_path = root / "state.yaml"
    if not state_path.exists():
        return default_state()

    state = default_state()
    section = ""
    for raw_line in state_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.rstrip()
        if not line or line.lstrip().startswith("#"):
            continue
        if not line.startswith(" ") and line.endswith(":"):
            section = line[:-1]
            continue
        match = re.match(r"^\s{2}([a-z_]+):\s*(.*)$", line)
        if not match:
            continue
        key, value = match.groups()
        value = value.strip().strip('"')
        if section == "workflow" and key in {"status", "started_at", "updated_at"}:
            state[key] = value
        elif section == "current" and key == "index":
            state["current_index"] = int(value or 0)
        elif section == "current" and key == "prompt_file":
            state["current_prompt"] = value
        elif section == "progress" and key in {"completed", "total"}:
            state[key] = int(value or 0)
    return state


def write_state(root: Path, state: dict[str, str | int]) -> None:
    text = f"""workflow:
  status: {state["status"]}
  started_at: {state["started_at"]}
  updated_at: {state["updated_at"]}

current:
  index: {state["current_index"]}
  prompt_file: {state["current_prompt"]}

progress:
  completed: {state["completed"]}
  total: {state["total"]}
"""
    (root / "state.yaml").write_text(text, encoding="utf-8")


def append_log(root: Path, message: str) -> None:
    log_path = root / "log.md"
    with log_path.open("a", encoding="utf-8") as handle:
        handle.write(f"- {now_iso()} {message}\n")


def require_root(cwd: Path) -> Path:
    root = workflow_root(cwd)
    if not root.exists():
        raise SystemExit("Mary Workflow is not initialized. Run /mw:init first.")
    return root


def cmd_init(args: argparse.Namespace) -> int:
    root = workflow_root(Path.cwd())
    root.mkdir(exist_ok=True)
    (root / PROMPTS_DIR).mkdir(exist_ok=True)

    config_path = root / "config.yaml"
    if not config_path.exists():
        config_path.write_text(
            "workflow:\n"
            "  name: Mary Workflow\n"
            "  prompt_glob: prompts/*.md\n"
            "output:\n"
            "  language: auto\n",
            encoding="utf-8",
        )

    prompts = prompt_files(root)
    if not prompts and args.with_examples:
        first = root / PROMPTS_DIR / "001-project-scan.md"
        second = root / PROMPTS_DIR / "002-improvement-plan.md"
        first.write_text(
            "Scan the current project structure and summarize the main components.\n",
            encoding="utf-8",
        )
        second.write_text(
            "Based on the project scan, propose a short improvement plan with concrete next steps.\n",
            encoding="utf-8",
        )
        prompts = prompt_files(root)

    state = default_state()
    state["total"] = len(prompts)
    if prompts:
        state["current_prompt"] = prompts[0]
    write_state(root, state)

    log_path = root / "log.md"
    if not log_path.exists():
        log_path.write_text("# Mary Workflow Log\n\n", encoding="utf-8")
    append_log(root, "initialized workflow")
    print(f"Initialized {WORKFLOW_DIR} with {len(prompts)} prompt(s).")
    return 0


def cmd_start(args: argparse.Namespace) -> int:
    root = require_root(Path.cwd())
    prompts = prompt_files(root)
    if not prompts:
        raise SystemExit("No prompt files found in .mary-workflow/prompts/.")
    state = read_state(root)
    state["status"] = "running"
    state["started_at"] = state["started_at"] or now_iso()
    state["updated_at"] = now_iso()
    state["total"] = len(prompts)
    completed = int(state["completed"])
    current_index = min(completed, len(prompts) - 1)
    state["current_index"] = current_index
    state["current_prompt"] = prompts[current_index]
    write_state(root, state)
    append_log(root, f"started workflow at {state['current_prompt']}")
    print_status(state)
    return 0


def cmd_status(args: argparse.Namespace) -> int:
    root = require_root(Path.cwd())
    state = read_state(root)
    prompts = prompt_files(root)
    if int(state["total"]) != len(prompts):
        state["total"] = len(prompts)
        if prompts and not state["current_prompt"]:
            state["current_prompt"] = prompts[min(int(state["completed"]), len(prompts) - 1)]
        write_state(root, state)
    print_status(state)
    return 0


def cmd_complete_current(args: argparse.Namespace) -> int:
    root = require_root(Path.cwd())
    prompts = prompt_files(root)
    if not prompts:
        raise SystemExit("No prompt files found in .mary-workflow/prompts/.")

    state = read_state(root)
    completed = min(int(state["completed"]) + 1, len(prompts))
    state["completed"] = completed
    state["total"] = len(prompts)
    state["updated_at"] = now_iso()

    if completed >= len(prompts):
        state["status"] = "completed"
        state["current_index"] = len(prompts)
        state["current_prompt"] = ""
        append_log(root, "completed final prompt")
    else:
        state["status"] = "running"
        state["current_index"] = completed
        state["current_prompt"] = prompts[completed]
        append_log(root, f"advanced to {state['current_prompt']}")

    write_state(root, state)
    print_status(state)
    return 0


def cmd_stop(args: argparse.Namespace) -> int:
    root = require_root(Path.cwd())
    state = read_state(root)
    state["status"] = "stopped"
    state["updated_at"] = now_iso()
    write_state(root, state)
    append_log(root, "stopped workflow")
    print_status(state)
    return 0


def print_status(state: dict[str, str | int]) -> None:
    prompt = state["current_prompt"] or "(none)"
    print(f"status: {state['status']}")
    print(f"progress: {state['completed']}/{state['total']}")
    print(f"current: {prompt}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Mary Workflow runtime helper")
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser("init", help="create .mary-workflow")
    init_parser.add_argument("--with-examples", action="store_true", help="create two starter prompts")
    init_parser.set_defaults(func=cmd_init)

    subparsers.add_parser("start", help="start workflow").set_defaults(func=cmd_start)
    subparsers.add_parser("status", help="show status").set_defaults(func=cmd_status)
    subparsers.add_parser("complete-current", help="mark current prompt complete").set_defaults(func=cmd_complete_current)
    subparsers.add_parser("stop", help="stop workflow").set_defaults(func=cmd_stop)
    return parser


def main(argv: list[str]) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
