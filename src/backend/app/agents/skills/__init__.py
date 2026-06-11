from __future__ import annotations

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[5]
SKILLS_DIR = Path(__file__).resolve().parent
TODODOT_TASK_WORKFLOW_SKILL = SKILLS_DIR / "todoodot-task-workflow"

# Use this with FilesystemBackend(root_dir=PROJECT_ROOT) or create_todoodot_agent.
DEEPAGENTS_SKILLS = ["/src/backend/app/agents/skills/"]


__all__ = [
    "DEEPAGENTS_SKILLS",
    "PROJECT_ROOT",
    "SKILLS_DIR",
    "TODODOT_TASK_WORKFLOW_SKILL",
]
