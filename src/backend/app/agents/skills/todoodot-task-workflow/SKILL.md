---
name: todoodot-task-workflow
description: >-
  Use this skill when managing local tasks, Jira issues, Confluence context, or
  todo workflows with the todoodot MCP tools: list_task, add_task,
  complete_task, and mcp-atlassian tools.
---

# Todoodot Task Workflow

## Overview

Use this skill to manage the user's local todo list and coordinate it with Jira
or Confluence context when available. The MCP tools perform actions; this skill
defines the workflow for choosing and sequencing those tools.

## Available Tool Expectations

- `list_task`: List local tasks. Use `include_completed=False` when checking active work.
- `add_task`: Add a local task with a clear title and optional description.
- `complete_task`: Mark a local task complete by id.
- `mcp-atlassian` tools: Use for Jira and Confluence lookup or updates when the user references Jira keys, tickets, projects, sprints, pages, or company docs.

## Workflow

1. For task creation, first call `list_task(include_completed=False)` to avoid duplicates when the user's request may already exist.
2. Use `add_task` for local todo creation. Keep the title short and action-oriented. Put Jira keys, links, acceptance criteria, due dates, or source context in the description.
3. If the user references a Jira key or Jira URL, fetch the Jira issue before adding or changing a task when credentials are available. Include the issue key and a concise summary in the local task description.
4. If the user references Confluence docs, fetch only the relevant page/context needed to make the task actionable. Do not copy large page contents into local task descriptions.
5. For completion, call `list_task(include_completed=False)` first unless the user gives an exact local task id. If multiple tasks match, ask a short clarification instead of guessing.
6. Use `complete_task` only for local tasks. Do not transition Jira issues unless the user explicitly asks for a Jira status change.
7. For Jira or Confluence writes, confirm intent when the request is ambiguous or could affect shared project state.

## Supporting Resources

Load these files only when the task needs the extra detail:

- `references/local-task-contract.md`: Read when unsure how to shape local task titles, descriptions, duplicate checks, or completion matching.
- `references/atlassian-workflow.md`: Read when the task mentions Jira keys, Jira URLs, Confluence pages, sprints, project docs, or shared Atlassian state.
- `scripts/format_task_description.py`: Use when building a local task description from several fields such as Jira key, URL, due date, context, and acceptance criteria.
- `assets/task-description-template.md`: Use as a manual description template when a script is unnecessary.

## Output Style

After tool use, reply with the completed action and the relevant id or title.
Keep summaries brief:

- Added: task id, title, and linked Jira key if any.
- Completed: task id and title.
- Listed: active tasks first, completed tasks only when requested.

If Atlassian credentials or tools are unavailable, continue with local task tools
and mention that Jira/Confluence enrichment was skipped.
