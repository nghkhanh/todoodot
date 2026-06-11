# Atlassian Workflow

Use this reference when the user mentions Jira, Confluence, sprints, project
docs, tickets, issues, epics, or Atlassian URLs.

## Jira Lookup

Fetch the Jira issue before creating a local task when the user provides:

- A Jira key such as `PROJ-123`.
- A Jira issue URL.
- A request like "add this Jira ticket as a task".

Use the issue summary as the task title when it is clearer than the user's raw
wording. Put the Jira key, URL, status, assignee, and relevant acceptance
criteria in the task description.

## Confluence Lookup

Fetch Confluence context only when it helps make the task actionable. Prefer
small, relevant excerpts or page metadata. Do not paste long page content into
local task descriptions.

## Writes and Shared State

Local task writes are safe to perform when requested. Jira or Confluence writes
can affect shared project state, so require clear user intent before:

- Transitioning Jira issue status.
- Adding comments to Jira.
- Editing Confluence pages.
- Creating or deleting Atlassian content.

If the user asks to complete a local task that came from Jira, only call
`complete_task` unless they explicitly ask to update Jira too.

## Missing Credentials

If Atlassian tools or credentials are unavailable, continue with local task
tools. Mention that Jira or Confluence enrichment was skipped and include the
raw key or URL the user provided.
