from __future__ import annotations

from typing import Any

from deepagents import create_deep_agent
from deepagents.backends.filesystem import FilesystemBackend

from app.agents.mcp_client import load_agent_tools
from app.agents.skills import DEEPAGENTS_SKILLS, PROJECT_ROOT
from app.services.llm_service import create_langchain_chat_model


async def create_todoodot_agent(
    model: Any | None = None,
    include_atlassian: bool = True,
    **kwargs: Any,
):
    tools = await load_agent_tools(include_atlassian=include_atlassian)
    backend = FilesystemBackend(root_dir=str(PROJECT_ROOT), virtual_mode=True)
    if model is None:
        chat_model = create_langchain_chat_model()
    elif isinstance(model, str) and model.startswith("openrouter/"):
        chat_model = create_langchain_chat_model(model=model)
    else:
        chat_model = model

    return create_deep_agent(
        model=chat_model,
        tools=tools,
        backend=backend,
        skills=DEEPAGENTS_SKILLS,
        **kwargs,
    )
