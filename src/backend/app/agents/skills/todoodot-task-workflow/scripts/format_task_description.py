#!/usr/bin/env python3
from __future__ import annotations

import argparse


def add_section(parts: list[str], title: str, lines: list[str]) -> None:
    clean_lines = [line.strip() for line in lines if line and line.strip()]
    if not clean_lines:
        return

    parts.append(f"{title}:")
    parts.extend(f"- {line}" for line in clean_lines)


def build_description(args: argparse.Namespace) -> str:
    parts: list[str] = []

    source_lines = []
    if args.jira_key:
        source_lines.append(f"Jira: {args.jira_key}")
    if args.jira_url:
        source_lines.append(f"Jira URL: {args.jira_url}")
    if args.confluence_url:
        source_lines.append(f"Confluence: {args.confluence_url}")
    add_section(parts, "Source", source_lines)

    add_section(parts, "Context", args.context)
    add_section(parts, "Due", [args.due_date] if args.due_date else [])
    add_section(parts, "Acceptance criteria", args.acceptance)
    add_section(parts, "Notes", args.note)

    return "\n".join(parts).strip()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Format a compact local task description."
    )
    parser.add_argument("--jira-key")
    parser.add_argument("--jira-url")
    parser.add_argument("--confluence-url")
    parser.add_argument("--due-date")
    parser.add_argument("--context", action="append", default=[])
    parser.add_argument("--acceptance", action="append", default=[])
    parser.add_argument("--note", action="append", default=[])
    return parser.parse_args()


def main() -> None:
    description = build_description(parse_args())
    if description:
        print(description)


if __name__ == "__main__":
    main()
