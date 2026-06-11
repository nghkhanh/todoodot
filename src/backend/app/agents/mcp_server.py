from __future__ import annotations

import asyncio
import sys
from typing import Any

from fastmcp import FastMCP

from app.agents.tools import (
    add_task as add_local_task,
    complete_task as complete_local_task,
    list_task as list_local_task,
)


mcp = FastMCP("todoodot-local")


@mcp.tool()
def list_task(include_completed: bool = True) -> list[dict[str, Any]]:
    """List local tasks."""
    return list_local_task(include_completed=include_completed)


@mcp.tool()
def add_task(title: str, description: str = "") -> dict[str, Any]:
    """Add a local task."""
    return add_local_task(title=title, description=description)


@mcp.tool()
def complete_task(task_id: int) -> dict[str, Any]:
    """Complete a local task by id."""
    return complete_local_task(task_id=task_id)


async def list_tool_names() -> list[str]:
    tools = await mcp.list_tools()
    return sorted(tool.name for tool in tools)


def print_tool_names() -> None:
    tool_names = asyncio.run(list_tool_names())
    print(f"Available tools: {', '.join(tool_names)}", file=sys.stderr)


if __name__ == "__main__":
    print_tool_names()
    mcp.run(transport="stdio")
