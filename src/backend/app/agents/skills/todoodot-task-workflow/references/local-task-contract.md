# Local Task Contract

Use this reference when creating, listing, deduplicating, or completing local
tasks with `list_task`, `add_task`, and `complete_task`.

## Task Shape

Local tasks are returned as dictionaries with these fields:

- `id`: integer local task id.
- `title`: short action-oriented title.
- `description`: optional detail text.
- `status`: `pending` or `completed`.
- `created_at`: UTC ISO timestamp.
- `completed_at`: UTC ISO timestamp or null.

## Title Rules

- Start with a verb when possible: "Review", "Create", "Fix", "Follow up".
- Keep the title scannable; put links, ticket keys, acceptance criteria, and
  longer context in `description`.
- If the task is derived from Jira, include the Jira key at the end or start of
  the title only if it improves scanability, for example `PROJ-123: Review API`.

## Description Rules

Use compact sections only when they add value:

- Source: Jira key, Jira URL, Confluence page, or user request.
- Context: concise summary of why the task exists.
- Due: explicit dates only; do not invent deadlines.
- Acceptance criteria: concrete checks from Jira, Confluence, or the user.
- Notes: blockers, assumptions, or follow-up details.

## Duplicate Checks

Before adding a task, call `list_task(include_completed=False)` and compare:

- Exact or near-exact title matches.
- Same Jira key or URL in title or description.
- Same concrete work item described with different wording.

If one clear duplicate exists, do not add a new task; report the existing task.
If several candidates match, ask a short clarification.

## Completion Matching

If the user gives a local task id, call `complete_task` directly. Otherwise,
call `list_task(include_completed=False)` and match by title, Jira key, or
source URL. Ask for clarification if more than one active task matches.
