__all__ = [
    "create_mcp_client",
    "create_todoodot_agent",
    "get_mcp_server_config",
    "load_agent_tools",
]


def __getattr__(name: str):
    if name == "create_todoodot_agent":
        from app.agents.deep_agent import create_todoodot_agent

        return create_todoodot_agent

    if name in {"create_mcp_client", "get_mcp_server_config", "load_agent_tools"}:
        from app.agents import mcp_client

        return getattr(mcp_client, name)

    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
