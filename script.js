/**
 * OPUS — Premium Task Manager
 * script.js  |  Vanilla JavaScript, modular & well-commented
 */

"use strict";

/* =====================================================
   1. STATE & CONSTANTS
   ===================================================== */

/** Priority sort weights for ordering */
const PRIORITY_WEIGHT = { high: 3, medium: 2, low: 1 };

/** Category emoji/label map */
const CAT_ICON = { work: "💼", study: "📚", personal: "🏠", other: "✨" };

/** App state — single source of truth */
const state = {
  tasks:        [],   // active tasks
  deletedTasks: [],   // soft-deleted tasks
  currentEdit:  null, // task id being edited
  historyTab:   "completed", // "completed" | "deleted"
  filters: {
    search:   "",
    status:   "all",
    priority: "all",
    category: "all",
    sort:     "date-asc",
  },
};

/* =====================================================
   2. LOCAL STORAGE HELPERS
   ===================================================== */

/** Persist state to localStorage */
function saveState() {
  localStorage.setItem("opus_tasks",   JSON.stringify(state.tasks));
  localStorage.setItem("opus_deleted", JSON.stringify(state.deletedTasks));
}

/** Load state from localStorage */
function loadState() {
  try {
    const tasks   = localStorage.getItem("opus_tasks");
    const deleted = localStorage.getItem("opus_deleted");
    if (tasks)   state.tasks        = JSON.parse(tasks);
    if (deleted) state.deletedTasks = JSON.parse(deleted);
  } catch (e) {
    console.error("Failed to load state:", e);
  }
}

/* =====================================================
   3. TASK CRUD
   ===================================================== */

/**
 * Generate a unique ID
 * @returns {string}
 */
function generateId() {
  return `task_${Date.now()}_${Math.random().toString(36).slice(2, 7)}`;
}

/**
 * Add a new task
 * @param {Object} data - form field values
 */
function addTask(data) {
  const task = {
    id:        generateId(),
    title:     data.title.trim(),
    desc:      data.desc.trim(),
    date:      data.date,
    time:      data.time,
    priority:  data.priority,
    category:  data.category,
    completed: false,
    createdAt: new Date().toISOString(),
  };
  state.tasks.unshift(task);
  saveState();
  renderTasks();
  updateStats();
  showToast("Task added successfully", "success");
  scheduleReminder(task);
}

/**
 * Update an existing task by id
 * @param {string} id
 * @param {Object} data
 */
function updateTask(id, data) {
  const idx = state.tasks.findIndex(t => t.id === id);
  if (idx === -1) return;
  state.tasks[idx] = {
    ...state.tasks[idx],
    title:    data.title.trim(),
    desc:     data.desc.trim(),
    date:     data.date,
    time:     data.time,
    priority: data.priority,
    category: data.category,
  };
  saveState();
  renderTasks();
  updateStats();
  showToast("Task updated", "info");
}

/**
 * Toggle task completion
 * @param {string} id
 */
function toggleComplete(id) {
  const task = state.tasks.find(t => t.id === id);
  if (!task) return;
  task.completed = !task.completed;
  if (task.completed) task.completedAt = new Date().toISOString();
  else delete task.completedAt;
  saveState();
  renderTasks();
  updateStats();
  showToast(
    task.completed ? "Task marked complete 🎉" : "Task reopened",
    task.completed ? "success" : "info"
  );
  if (state.historyTab === "completed") renderHistory();
}

/**
 * Soft-delete a task (moves to history)
 * @param {string} id
 */
function deleteTask(id) {
  const idx = state.tasks.findIndex(t => t.id === id);
  if (idx === -1) return;
  const [removed] = state.tasks.splice(idx, 1);
  removed.deletedAt = new Date().toISOString();
  state.deletedTasks.unshift(removed);
  saveState();
  renderTasks();
  renderHistory();
  updateStats();
  showToast("Task deleted", "warning");
}

/**
 * Permanently remove a task from history
 * @param {string} id
 * @param {"deleted"|"completed"} source
 */
function removeFromHistory(id, source) {
  if (source === "deleted") {
    state.deletedTasks = state.deletedTasks.filter(t => t.id !== id);
  } else {
    // remove from active tasks (completed)
    state.tasks = state.tasks.filter(t => t.id !== id);
  }
  saveState();
  renderHistory();
  updateStats();
  showToast("Permanently removed", "warning");
}

/**
 * Clear ALL active tasks
 */
function clearAllTasks() {
  // Move all to deleted
  const ts = new Date().toISOString();
  state.tasks.forEach(t => {
    t.deletedAt = ts;
    state.deletedTasks.unshift(t);
  });
  state.tasks = [];
  saveState();
  renderTasks();
  renderHistory();
  updateStats();
  showToast("All tasks cleared", "warning");
}

/* =====================================================
   4. FILTERING & SORTING
   ===================================================== */

/**
 * Apply current filters + sort to tasks array
 * @returns {Array}
 */
function getFilteredTasks() {
  const { search, status, priority, category, sort } = state.filters;
  const q = search.toLowerCase();

  let result = state.tasks.filter(t => {
    const matchSearch   = !q || t.title.toLowerCase().includes(q) || t.desc.toLowerCase().includes(q);
    const matchStatus   = status === "all" || (status === "completed" ? t.completed : !t.completed);
    const matchPriority = priority === "all" || t.priority === priority;
    const matchCategory = category === "all" || t.category === category;
    return matchSearch && matchStatus && matchPriority && matchCategory;
  });

  // Sorting
  result.sort((a, b) => {
    switch (sort) {
      case "date-asc":       return new Date(a.date) - new Date(b.date);
      case "date-desc":      return new Date(b.date) - new Date(a.date);
      case "priority-high":  return PRIORITY_WEIGHT[b.priority] - PRIORITY_WEIGHT[a.priority];
      case "priority-low":   return PRIORITY_WEIGHT[a.priority] - PRIORITY_WEIGHT[b.priority];
      case "alpha":          return a.title.localeCompare(b.title);
      default:               return 0;
    }
  });

  return result;
}

/* =====================================================
   5. RENDER FUNCTIONS
   ===================================================== */

/**
 * Render the active task list
 */
function renderTasks() {
  const list     = document.getElementById("task-list");
  const empty    = document.getElementById("empty-state");
  const filtered = getFilteredTasks();

  list.innerHTML = "";

  if (filtered.length === 0) {
    empty.hidden = false;
  } else {
    empty.hidden = true;
    filtered.forEach(task => list.appendChild(createTaskCard(task, false)));
  }
}

/**
 * Render history (completed or deleted)
 */
function renderHistory() {
  const list    = document.getElementById("history-list");
  const empty   = document.getElementById("history-empty");
  const tab     = state.historyTab;

  // Update badges
  const completedTasks = state.tasks.filter(t => t.completed);
  document.getElementById("badge-completed").textContent = completedTasks.length;
  document.getElementById("badge-deleted").textContent   = state.deletedTasks.length;

  list.innerHTML = "";

  const items = tab === "completed"
    ? completedTasks
    : state.deletedTasks;

  if (items.length === 0) {
    empty.hidden = false;
  } else {
    empty.hidden = true;
    items.forEach(task => list.appendChild(createTaskCard(task, true)));
  }
}

/**
 * Build a task card DOM element
 * @param {Object} task
 * @param {boolean} isHistory
 * @returns {HTMLElement}
 */
function createTaskCard(task, isHistory) {
  const card = document.createElement("article");
  card.className   = "task-card" + (task.completed ? " completed" : "") + (isHistory ? " history-card" : "");
  card.dataset.id       = task.id;
  card.dataset.priority = task.priority;
  card.setAttribute("role", "listitem");

  // Format date/time
  const dateStr = task.date ? formatDate(task.date) : "";
  const timeStr = task.time || "";

  // Priority tag class
  const priorityClass = `tag-priority-${task.priority}`;
  const priorityLabel = task.priority.charAt(0).toUpperCase() + task.priority.slice(1);

  // Checkbox (hidden in history)
  const checkHtml = isHistory
    ? `<div class="task-check-placeholder" style="width:22px"></div>`
    : `<input type="checkbox" class="task-check" aria-label="Mark complete"
         ${task.completed ? "checked" : ""} data-id="${task.id}" />`;

  // Action buttons
  let actionsHtml = "";
  if (isHistory) {
    actionsHtml = `
      <div class="task-actions">
        <button class="action-btn delete" data-id="${task.id}" data-source="${state.historyTab}"
          title="Remove permanently" aria-label="Remove permanently">
          <i class="ph ph-trash-simple"></i>
        </button>
      </div>`;
  } else {
    actionsHtml = `
      <div class="task-actions">
        <button class="action-btn edit" data-id="${task.id}" title="Edit task" aria-label="Edit task">
          <i class="ph ph-pencil-simple"></i>
        </button>
        <button class="action-btn delete" data-id="${task.id}" title="Delete task" aria-label="Delete task">
          <i class="ph ph-trash-simple"></i>
        </button>
      </div>`;
  }

  card.innerHTML = `
    ${checkHtml}
    <div class="task-body">
      <div class="task-title">${escapeHtml(task.title)}</div>
      ${task.desc ? `<div class="task-desc">${escapeHtml(task.desc)}</div>` : ""}
      <div class="task-meta">
        ${dateStr ? `<span class="tag tag-date"><i class="ph ph-calendar-blank"></i>${dateStr}</span>` : ""}
        ${timeStr ? `<span class="tag tag-time"><i class="ph ph-clock"></i>${timeStr}</span>` : ""}
        <span class="tag ${priorityClass}">${priorityLabel}</span>
        <span class="tag tag-cat">${CAT_ICON[task.category] || "📌"} ${capitalize(task.category)}</span>
      </div>
    </div>
    ${actionsHtml}
  `;

  return card;
}

/**
 * Update dashboard stats + progress bar
 */
function updateStats() {
  const total     = state.tasks.length;
  const completed = state.tasks.filter(t => t.completed).length;
  const pending   = total - completed;
  const highPri   = state.tasks.filter(t => t.priority === "high" && !t.completed).length;
  const pct       = total === 0 ? 0 : Math.round((completed / total) * 100);

  document.getElementById("stat-total").textContent     = total;
  document.getElementById("stat-completed").textContent = completed;
  document.getElementById("stat-pending").textContent   = pending;
  document.getElementById("stat-high").textContent      = highPri;
  document.getElementById("progress-pct").textContent   = `${pct}%`;
  document.getElementById("progress-fill").style.width  = `${pct}%`;
}

/* =====================================================
   6. FORM HANDLING
   ===================================================== */

/** Open the task modal for adding */
function openAddModal() {
  state.currentEdit = null;
  const form = document.getElementById("task-form");
  form.reset();
  clearFormErrors();
  document.getElementById("task-id").value     = "";
  document.getElementById("modal-title").textContent  = "New Task";
  document.getElementById("submit-label").textContent = "Add Task";
  // Default date = today
  document.getElementById("task-date").value = todayISO();
  showModal("task-modal");
}

/** Open the task modal for editing */
function openEditModal(id) {
  const task = state.tasks.find(t => t.id === id);
  if (!task) return;
  state.currentEdit = id;

  document.getElementById("task-id").value          = task.id;
  document.getElementById("task-title").value       = task.title;
  document.getElementById("task-desc").value        = task.desc;
  document.getElementById("task-date").value        = task.date;
  document.getElementById("task-time").value        = task.time;
  document.getElementById("task-priority").value    = task.priority;
  document.getElementById("task-category").value    = task.category;

  document.getElementById("modal-title").textContent  = "Edit Task";
  document.getElementById("submit-label").textContent = "Save Changes";
  clearFormErrors();
  showModal("task-modal");
}

/** Handle form submission */
function handleFormSubmit(e) {
  e.preventDefault();

  const title = document.getElementById("task-title").value;
  const date  = document.getElementById("task-date").value;

  if (!validateForm(title, date)) return;

  const data = {
    title:    title,
    desc:     document.getElementById("task-desc").value,
    date:     date,
    time:     document.getElementById("task-time").value,
    priority: document.getElementById("task-priority").value,
    category: document.getElementById("task-category").value,
  };

  if (state.currentEdit) {
    updateTask(state.currentEdit, data);
  } else {
    addTask(data);
  }

  hideModal("task-modal");
}

/** Validate required fields, show inline errors */
function validateForm(title, date) {
  let valid = true;
  clearFormErrors();

  if (!title.trim()) {
    showFieldError("title-error", "task-title", "Task title is required");
    valid = false;
  } else if (title.trim().length < 2) {
    showFieldError("title-error", "task-title", "Title must be at least 2 characters");
    valid = false;
  }

  if (!date) {
    showFieldError("date-error", "task-date", "Please select a date");
    valid = false;
  }

  return valid;
}

function showFieldError(errorId, inputId, msg) {
  document.getElementById(errorId).textContent = msg;
  document.getElementById(inputId).classList.add("error");
}

function clearFormErrors() {
  ["title-error", "date-error"].forEach(id => {
    const el = document.getElementById(id);
    if (el) el.textContent = "";
  });
  ["task-title", "task-date"].forEach(id => {
    const el = document.getElementById(id);
    if (el) el.classList.remove("error");
  });
}

/* =====================================================
   7. MODAL HELPERS
   ===================================================== */

function showModal(id) {
  const el = document.getElementById(id);
  el.hidden = false;
  el.setAttribute("aria-hidden", "false");
  // Trap focus on first focusable
  const first = el.querySelector("input, button, select, textarea");
  if (first) setTimeout(() => first.focus(), 50);
}

function hideModal(id) {
  const el = document.getElementById(id);
  el.hidden = true;
  el.setAttribute("aria-hidden", "true");
}

/** Generic confirmation dialog — returns a Promise */
function confirm(message, confirmLabel = "Delete") {
  return new Promise(resolve => {
    document.getElementById("confirm-message").textContent = message;
    document.getElementById("confirm-ok").textContent     = confirmLabel;
    showModal("confirm-modal");

    const okBtn     = document.getElementById("confirm-ok");
    const cancelBtn = document.getElementById("confirm-cancel");

    function cleanup(result) {
      hideModal("confirm-modal");
      okBtn.removeEventListener("click", onOk);
      cancelBtn.removeEventListener("click", onCancel);
      resolve(result);
    }
    function onOk()     { cleanup(true);  }
    function onCancel() { cleanup(false); }

    okBtn.addEventListener("click", onOk);
    cancelBtn.addEventListener("click", onCancel);
  });
}

/* =====================================================
   8. TOAST NOTIFICATIONS
   ===================================================== */

const TOAST_ICONS = {
  success: "ph-check-circle",
  error:   "ph-x-circle",
  info:    "ph-info",
  warning: "ph-warning",
};

/**
 * Show a toast notification
 * @param {string} message
 * @param {"success"|"error"|"info"|"warning"} type
 * @param {number} duration  ms before auto-dismiss
 */
function showToast(message, type = "info", duration = 3000) {
  const container = document.getElementById("toast-container");
  const toast     = document.createElement("div");
  toast.className = `toast ${type}`;
  toast.innerHTML = `
    <i class="ph ${TOAST_ICONS[type]} toast-icon"></i>
    <span>${escapeHtml(message)}</span>
  `;
  container.appendChild(toast);

  setTimeout(() => {
    toast.classList.add("removing");
    toast.addEventListener("animationend", () => toast.remove());
  }, duration);
}

/* =====================================================
   9. REMINDER / NOTIFICATION
   ===================================================== */

/**
 * Schedule an alert reminder for a task's due time
 * @param {Object} task
 */
function scheduleReminder(task) {
  if (!task.date || !task.time) return;

  const dueDate  = new Date(`${task.date}T${task.time}`);
  const now      = new Date();
  const diff     = dueDate.getTime() - now.getTime();

  if (diff <= 0) return; // already past

  // Remind 5 minutes before
  const remind5  = diff - 5 * 60 * 1000;
  if (remind5 > 0) {
    setTimeout(() => {
      // Check it's still active and not completed
      const live = state.tasks.find(t => t.id === task.id);
      if (live && !live.completed) {
        showToast(`⏰ Reminder: "${task.title}" is due in 5 min!`, "warning", 8000);
        alert(`⏰ OPUS Reminder\n\nTask: "${task.title}"\nDue in 5 minutes!`);
      }
    }, remind5);
  }

  // Alert at exact due time
  setTimeout(() => {
    const live = state.tasks.find(t => t.id === task.id);
    if (live && !live.completed) {
      showToast(`🔔 Task due now: "${task.title}"`, "error", 8000);
      alert(`🔔 OPUS — Task Due Now!\n\nTask: "${task.title}"\nTime's up!`);
    }
  }, diff);
}

/* =====================================================
   10. IMPORT / EXPORT
   ===================================================== */

/** Export tasks to a downloadable JSON file */
function exportTasks() {
  const data = {
    exportedAt: new Date().toISOString(),
    tasks:      state.tasks,
    deletedTasks: state.deletedTasks,
  };
  const blob = new Blob([JSON.stringify(data, null, 2)], { type: "application/json" });
  const url  = URL.createObjectURL(blob);
  const a    = document.createElement("a");
  a.href     = url;
  a.download = `opus-tasks-${todayISO()}.json`;
  a.click();
  URL.revokeObjectURL(url);
  showToast("Tasks exported successfully", "success");
}

/** Import tasks from a JSON file */
function importTasks(file) {
  if (!file) return;
  const reader = new FileReader();
  reader.onload = e => {
    try {
      const data = JSON.parse(e.target.result);

      // Support both wrapped format and raw array
      const imported = Array.isArray(data) ? data : (data.tasks || []);
      if (!Array.isArray(imported)) throw new Error("Invalid format");

      // Merge — avoid duplicate IDs
      const existingIds = new Set(state.tasks.map(t => t.id));
      let count = 0;
      imported.forEach(t => {
        if (t && t.id && t.title && !existingIds.has(t.id)) {
          state.tasks.push(t);
          count++;
        }
      });

      // Also import deleted if present
      if (data.deletedTasks && Array.isArray(data.deletedTasks)) {
        const existingDelIds = new Set(state.deletedTasks.map(t => t.id));
        data.deletedTasks.forEach(t => {
          if (t && t.id && !existingDelIds.has(t.id)) {
            state.deletedTasks.push(t);
          }
        });
      }

      saveState();
      renderTasks();
      renderHistory();
      updateStats();
      showToast(`Imported ${count} task${count !== 1 ? "s" : ""}`, "success");
    } catch (err) {
      showToast("Invalid JSON file", "error");
    }
  };
  reader.readAsText(file);
  // Reset input so same file can be re-imported
  document.getElementById("import-input").value = "";
}

/* =====================================================
   11. THEME TOGGLE
   ===================================================== */

function applyTheme(theme) {
  document.documentElement.setAttribute("data-theme", theme);
  localStorage.setItem("opus_theme", theme);
  document.getElementById("theme-icon").className  = theme === "dark" ? "ph ph-moon" : "ph ph-sun";
  document.getElementById("theme-label").textContent = theme === "dark" ? "Dark Mode" : "Light Mode";
}

function toggleTheme() {
  const current = document.documentElement.getAttribute("data-theme") || "dark";
  applyTheme(current === "dark" ? "light" : "dark");
}

/* =====================================================
   12. VIEW SWITCHING
   ===================================================== */

function switchView(view) {
  // Nav items
  document.querySelectorAll(".nav-item[data-view]").forEach(btn => {
    btn.classList.toggle("active", btn.dataset.view === view);
  });

  // Sections
  document.getElementById("view-tasks").hidden   = view !== "tasks";
  document.getElementById("view-history").hidden = view !== "history";

  // Title
  document.getElementById("view-title").textContent =
    view === "tasks" ? "Dashboard" : "Task History";

  if (view === "history") renderHistory();
}

/* =====================================================
   13. UTILITY FUNCTIONS
   ===================================================== */

/** Format ISO date string to readable form */
function formatDate(iso) {
  if (!iso) return "";
  const [y, m, d] = iso.split("-");
  const months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"];
  return `${months[parseInt(m,10)-1]} ${parseInt(d,10)}, ${y}`;
}

/** Today's date as YYYY-MM-DD */
function todayISO() {
  return new Date().toISOString().split("T")[0];
}

/** Capitalize first letter */
function capitalize(str) {
  return str ? str.charAt(0).toUpperCase() + str.slice(1) : "";
}

/** Escape HTML to prevent XSS */
function escapeHtml(str) {
  return String(str)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

/** Set today's date in subtitle */
function setDateSubtitle() {
  const now     = new Date();
  const options = { weekday: "long", year: "numeric", month: "long", day: "numeric" };
  document.getElementById("view-date").textContent = now.toLocaleDateString(undefined, options);
}

/* =====================================================
   14. EVENT WIRING
   ===================================================== */

function initEvents() {
  /* ── Add task button ── */
  document.getElementById("add-task-btn").addEventListener("click", openAddModal);

  /* ── Task form submission ── */
  document.getElementById("task-form").addEventListener("submit", handleFormSubmit);

  /* ── Modal close buttons ── */
  document.getElementById("modal-close").addEventListener("click", () => hideModal("task-modal"));
  document.getElementById("form-cancel").addEventListener("click", () => hideModal("task-modal"));

  /* ── Close modal on overlay click ── */
  document.getElementById("task-modal").addEventListener("click", e => {
    if (e.target === e.currentTarget) hideModal("task-modal");
  });

  /* ── Task list — delegated click ── */
  document.getElementById("task-list").addEventListener("click", handleTaskListClick);

  /* ── History list — delegated click ── */
  document.getElementById("history-list").addEventListener("click", handleHistoryListClick);

  /* ── Search input ── */
  const searchInput = document.getElementById("search-input");
  const clearSearch = document.getElementById("clear-search");
  searchInput.addEventListener("input", () => {
    state.filters.search = searchInput.value;
    clearSearch.hidden   = !searchInput.value;
    renderTasks();
  });
  clearSearch.addEventListener("click", () => {
    searchInput.value    = "";
    state.filters.search = "";
    clearSearch.hidden   = true;
    renderTasks();
  });

  /* ── Filter dropdowns ── */
  document.getElementById("filter-status").addEventListener("change", e => {
    state.filters.status = e.target.value;
    renderTasks();
  });
  document.getElementById("filter-priority").addEventListener("change", e => {
    state.filters.priority = e.target.value;
    renderTasks();
  });
  document.getElementById("filter-category").addEventListener("change", e => {
    state.filters.category = e.target.value;
    renderTasks();
  });
  document.getElementById("sort-tasks").addEventListener("change", e => {
    state.filters.sort = e.target.value;
    renderTasks();
  });

  /* ── Clear all ── */
  document.getElementById("clear-all-btn").addEventListener("click", async () => {
    if (state.tasks.length === 0) { showToast("No tasks to clear", "info"); return; }
    const ok = await confirm(`Clear all ${state.tasks.length} task(s)? They'll move to history.`, "Clear All");
    if (ok) clearAllTasks();
  });

  /* ── Theme toggle ── */
  document.getElementById("theme-toggle").addEventListener("click", toggleTheme);

  /* ── Sidebar nav ── */
  document.querySelectorAll(".nav-item[data-view]").forEach(btn => {
    btn.addEventListener("click", () => switchView(btn.dataset.view));
  });

  /* ── History tabs ── */
  document.querySelectorAll(".history-tab").forEach(tab => {
    tab.addEventListener("click", () => {
      document.querySelectorAll(".history-tab").forEach(t => t.classList.remove("active"));
      tab.classList.add("active");
      state.historyTab = tab.dataset.htab;
      renderHistory();
    });
  });

  /* ── Export ── */
  document.getElementById("export-btn").addEventListener("click", exportTasks);

  /* ── Import ── */
  document.getElementById("import-input").addEventListener("change", e => {
    importTasks(e.target.files[0]);
  });

  /* ── Keyboard: Escape closes modal ── */
  document.addEventListener("keydown", e => {
    if (e.key === "Escape") {
      if (!document.getElementById("task-modal").hidden)   hideModal("task-modal");
      if (!document.getElementById("confirm-modal").hidden) hideModal("confirm-modal");
    }
  });
}

/* ─ Delegated handlers ──────────────────────────────── */

async function handleTaskListClick(e) {
  const editBtn   = e.target.closest(".action-btn.edit");
  const deleteBtn = e.target.closest(".action-btn.delete");
  const checkbox  = e.target.closest(".task-check");

  if (editBtn) {
    openEditModal(editBtn.dataset.id);
  } else if (deleteBtn) {
    const ok = await confirm("Delete this task? It'll be saved in history.", "Delete");
    if (ok) deleteTask(deleteBtn.dataset.id);
  } else if (checkbox) {
    toggleComplete(checkbox.dataset.id);
  }
}

async function handleHistoryListClick(e) {
  const deleteBtn = e.target.closest(".action-btn.delete");
  if (deleteBtn) {
    const ok = await confirm("Permanently delete this record? This cannot be undone.", "Delete");
    if (ok) removeFromHistory(deleteBtn.dataset.id, deleteBtn.dataset.source);
  }
}

/* =====================================================
   15. INIT
   ===================================================== */

function init() {
  // Load persisted data
  loadState();

  // Apply saved theme
  const savedTheme = localStorage.getItem("opus_theme") || "dark";
  applyTheme(savedTheme);

  // Set date in topbar
  setDateSubtitle();

  // Attach all event listeners
  initEvents();

  // Initial render
  renderTasks();
  updateStats();
}

// Boot the app when DOM is ready
document.addEventListener("DOMContentLoaded", init);