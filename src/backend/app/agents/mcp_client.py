from __future__ import annotations

import argparse
import asyncio
import os
from pathlib import Path
from typing import Any

from langchain_mcp_adapters.client import MultiServerMCPClient


BACKEND_DIR = Path(__file__).resolve().parents[2]


def _env(name: str, default: str) -> str:
    return os.getenv(name, default)


def get_local_mcp_server_config() -> dict[str, Any]:
    return {
        "transport": "stdio",
        "command": "uv",
        "args": [
            "--directory",
            str(BACKEND_DIR),
            "run",
            "python",
            "-m",
            "app.agents.mcp_server",
        ],
    }


def get_atlassian_mcp_server_config() -> dict[str, Any]:
    return {
        "transport": "stdio",
        "command": "uvx",
        "args": ["mcp-atlassian"],
        "env": {
            "JIRA_URL": _env("JIRA_URL", "https://your-company.atlassian.net"),
            "JIRA_USERNAME": _env("JIRA_USERNAME", "your.email@company.com"),
            "JIRA_API_TOKEN": _env("JIRA_API_TOKEN", "your_api_token"),
            "CONFLUENCE_URL": _env(
                "CONFLUENCE_URL",
                "https://your-company.atlassian.net/wiki",
            ),
            "CONFLUENCE_USERNAME": _env(
                "CONFLUENCE_USERNAME",
                "your.email@company.com",
            ),
            "CONFLUENCE_API_TOKEN": _env(
                "CONFLUENCE_API_TOKEN",
                "your_api_token",
            ),
        },
    }


def get_mcp_server_config(
    include_atlassian: bool = True,
) -> dict[str, dict[str, Any]]:
    config = {"todoodot-local": get_local_mcp_server_config()}

    if include_atlassian:
        config["mcp-atlassian"] = get_atlassian_mcp_server_config()

    return config


def create_mcp_client(include_atlassian: bool = True) -> MultiServerMCPClient:
    return MultiServerMCPClient(get_mcp_server_config(include_atlassian))


async def load_agent_tools(include_atlassian: bool = True):
    client = create_mcp_client(include_atlassian)
    return await client.get_tools()


async def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--include-atlassian",
        action="store_true",
        help="Also load tools from mcp-atlassian.",
    )
    args = parser.parse_args()

    tools = await load_agent_tools(include_atlassian=args.include_atlassian)
    print(sorted(tool.name for tool in tools))


if __name__ == "__main__":
    asyncio.run(main())
