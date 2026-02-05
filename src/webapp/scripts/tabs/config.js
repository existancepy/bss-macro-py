/*
=============================================
Config Tab
=============================================
*/

async function switchConfigTab(target) {
  //remove the active classes and hide all tabs
  Array.from(document.getElementsByClassName("settings-tab-item")).forEach(
    (x) => {
      x.classList.remove("active");
      document.getElementById(x.id.split("-")[1]).style.display = "none";
    }
  );
  //add active class
  target.classList.add("active");
  //get the element of the page to show
  const showElement = document.getElementById(target.id.split("-")[1]);
  showElement.style.display = "block";
  //scroll back to top
  showElement.scrollTo(0, 0);
}

async function loadConfig() {
  const settings = await loadAllSettings();
  loadInputs(settings);

  // Start with bss tab
  switchConfigTab(document.getElementById("setting-bss"));

  // Initialize drag and drop for priority list
  initializeDragAndDrop();

  // Initialize search functionality
  initializePrioritySearch();

  // Initialize quick action buttons
  initializeQuickActions();
}

function initializeDragAndDrop() {
  const dragContainers = document.querySelectorAll(".drag-list-container");

  dragContainers.forEach((container) => {
    let draggedElement = null;

    container.addEventListener("dragstart", (e) => {
      draggedElement = e.target.closest(".drag-item");
      if (draggedElement) {
        draggedElement.classList.add("dragging");
        e.dataTransfer.effectAllowed = "move";
        e.dataTransfer.setData("text/html", draggedElement.outerHTML);
      }
    });

    container.addEventListener("dragend", (e) => {
      if (draggedElement) {
        draggedElement.classList.remove("dragging");
        draggedElement = null;
        saveDragOrder(container);
      }
    });

    container.addEventListener("dragover", (e) => {
      e.preventDefault();
      e.dataTransfer.dropEffect = "move";

      const afterElement = getDragAfterElement(container, e.clientY);
      const draggable = document.querySelector(".dragging");

      if (afterElement == null) {
        container.appendChild(draggable);
      } else {
        container.insertBefore(draggable, afterElement);
      }
    });

    container.addEventListener("dragenter", (e) => {
      e.preventDefault();
    });

    container.addEventListener("drop", (e) => {
      e.preventDefault();
    });
  });
}

function getDragAfterElement(container, y) {
  const draggableElements = [
    ...container.querySelectorAll(".drag-item:not(.dragging)"),
  ];

  return draggableElements.reduce(
    (closest, child) => {
      const box = child.getBoundingClientRect();
      const offset = y - box.top - box.height / 2;

      if (offset < 0 && offset > closest.offset) {
        return { offset: offset, element: child };
      } else {
        return closest;
      }
    },
    { offset: Number.NEGATIVE_INFINITY }
  ).element;
}

function saveDragOrder(container) {
  const items = container.querySelectorAll(".drag-item:not(.hidden)");
  const order = Array.from(items).map((item) => item.dataset.id);

  // Save to settings
  const data = { task_priority_order: order };
  eel.saveDictProfileSettings(data);
}

function initializePrioritySearch() {
  const searchInput = document.getElementById("priority-search-input");
  if (!searchInput) return;

  searchInput.addEventListener("input", (e) => {
    const searchTerm = e.target.value.toLowerCase().trim();
    const container = document.getElementById("task_priority_order-container");
    if (!container) return;

    const items = container.querySelectorAll(".drag-item");
    items.forEach((item) => {
      const text =
        item.querySelector(".drag-text")?.textContent.toLowerCase() || "";
      if (searchTerm === "" || text.includes(searchTerm)) {
        item.classList.remove("hidden");
      } else {
        item.classList.add("hidden");
      }
    });
  });
}

function initializeQuickActions() {
  // Handle move to top buttons
  document.addEventListener("click", (e) => {
    if (e.target.classList.contains("move-to-top")) {
      const item = e.target.closest(".drag-item");
      const container = item?.parentElement;
      if (container && item) {
        container.insertBefore(item, container.firstChild);
        saveDragOrder(container);
      }
    }

    // Handle move to bottom buttons
    if (e.target.classList.contains("move-to-bottom")) {
      const item = e.target.closest(".drag-item");
      const container = item?.parentElement;
      if (container && item) {
        container.appendChild(item);
        saveDragOrder(container);
      }
    }
  });
}

$("#config-placeholder", loadConfig)
  .load("../htmlImports/tabs/config.html") //load config tab
  .on("click", ".settings-tab-item", (event) =>
    switchConfigTab(event.currentTarget)
  ); //navigate between fields
