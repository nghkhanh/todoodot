const STORAGE_KEY = "todoodot.frontend.tasks";

const form = document.querySelector("#task-form");
const titleInput = document.querySelector("#task-title");
const descriptionInput = document.querySelector("#task-description");
const taskList = document.querySelector("#task-list");
const emptyState = document.querySelector("#empty-state");
const taskCount = document.querySelector("#task-count");
const output = document.querySelector("#tool-output");
const seedButton = document.querySelector("#seed-button");
const filterButtons = Array.from(document.querySelectorAll("[data-filter]"));

let filter = "active";

function now() {
  return new Date().toISOString();
}

function readTasks() {
  const raw = window.localStorage.getItem(STORAGE_KEY);
  if (!raw) return [];

  try {
    const parsed = JSON.parse(raw);
    return Array.isArray(parsed) ? parsed : [];
  } catch {
    return [];
  }
}

function writeTasks(tasks) {
  window.localStorage.setItem(STORAGE_KEY, JSON.stringify(tasks, null, 2));
}

function listTask(includeCompleted = true) {
  const tasks = readTasks();
  return includeCompleted
    ? tasks
    : tasks.filter((task) => task.status !== "completed");
}

function addTask(title, description = "") {
  const tasks = readTasks();
  const maxId = tasks.reduce((id, task) => Math.max(id, Number(task.id) || 0), 0);
  const task = {
    id: maxId + 1,
    title: title.trim(),
    description: description.trim(),
    status: "pending",
    created_at: now(),
    completed_at: null,
  };

  if (!task.title) {
    throw new Error("Task title is required.");
  }

  tasks.push(task);
  writeTasks(tasks);
  setToolOutput("add_task", { title: task.title, description: task.description }, task);
  return task;
}

function completeTask(taskId) {
  const tasks = readTasks();
  const task = tasks.find((item) => Number(item.id) === Number(taskId));

  if (!task) {
    throw new Error(`Task not found: ${taskId}`);
  }

  task.status = "completed";
  task.completed_at = now();
  writeTasks(tasks);
  setToolOutput("complete_task", { task_id: Number(taskId) }, task);
  return task;
}

function setToolOutput(toolName, args, result) {
  output.textContent = JSON.stringify(
    {
      tool: toolName,
      args,
      result,
    },
    null,
    2,
  );
}

function formatDate(value) {
  if (!value) return "";
  return new Intl.DateTimeFormat(undefined, {
    month: "short",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
  }).format(new Date(value));
}

function getVisibleTasks() {
  const tasks = readTasks();
  if (filter === "active") return tasks.filter((task) => task.status !== "completed");
  if (filter === "completed") return tasks.filter((task) => task.status === "completed");
  return tasks;
}

function updateCount() {
  const activeCount = listTask(false).length;
  const label = activeCount === 1 ? "active" : "active";
  taskCount.textContent = `${activeCount} ${label}`;
}

function renderTasks() {
  const tasks = getVisibleTasks();
  taskList.replaceChildren();
  emptyState.classList.toggle("is-visible", tasks.length === 0);
  updateCount();

  for (const task of tasks) {
    const card = document.createElement("article");
    card.className = `task-card${task.status === "completed" ? " is-completed" : ""}`;

    const content = document.createElement("div");

    const title = document.createElement("div");
    title.className = "task-title";
    title.textContent = task.title;
    content.append(title);

    if (task.description) {
      const description = document.createElement("div");
      description.className = "task-description";
      description.textContent = task.description;
      content.append(description);
    }

    const meta = document.createElement("div");
    meta.className = "task-meta";
    meta.append(makeMeta(`#${task.id}`));
    meta.append(makeMeta(task.status));
    meta.append(makeMeta(formatDate(task.created_at)));
    content.append(meta);

    const button = document.createElement("button");
    button.className = "complete-button";
    button.type = "button";
    button.textContent = task.status === "completed" ? "Done" : "Complete";
    button.disabled = task.status === "completed";
    button.addEventListener("click", () => {
      completeTask(task.id);
      renderTasks();
    });

    card.append(content, button);
    taskList.append(card);
  }
}

function makeMeta(text) {
  const item = document.createElement("span");
  item.textContent = text;
  return item;
}

function setFilter(nextFilter) {
  filter = nextFilter;
  for (const button of filterButtons) {
    button.classList.toggle("is-active", button.dataset.filter === filter);
  }
  setToolOutput("list_task", { include_completed: filter !== "active" }, getVisibleTasks());
  renderTasks();
}

function seedTasks() {
  const existing = readTasks();
  const samples = [
    ["Review MCP server", "Confirm list_task, add_task, complete_task are visible."],
    ["Test DeepAgents skill", "Check task workflow resource loading."],
    ["Wire OpenRouter key", "Set OPENROUTER_API_KEY before running the agent."],
  ];

  for (const [title, description] of samples) {
    const duplicate = existing.some((task) => task.title === title);
    if (!duplicate) addTask(title, description);
  }

  setFilter("active");
}

form.addEventListener("submit", (event) => {
  event.preventDefault();
  addTask(titleInput.value, descriptionInput.value);
  form.reset();
  titleInput.focus();
  renderTasks();
});

seedButton.addEventListener("click", seedTasks);

for (const button of filterButtons) {
  button.addEventListener("click", () => setFilter(button.dataset.filter));
}

setToolOutput("list_task", { include_completed: false }, listTask(false));
renderTasks();
