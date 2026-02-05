/*
=============================================
Profiles Tab
=============================================
*/

async function loadProfiles() {
  const settings = await loadAllSettings();
  loadInputs(settings);

  // Load profile list
  await loadProfileList();

  // Set up file input event listener after HTML is loaded
  setupFileInputListener();
}

/*
=============================================
Profile Management
=============================================
*/

async function loadProfileList() {
  try {
    const profiles = await eel.listProfiles()();
    const currentProfile = await eel.getCurrentProfile()();

    // Update current profile display
    const currentProfileDisplay = document.getElementById(
      "current-profile-display"
    );
    if (currentProfileDisplay) {
      currentProfileDisplay.textContent = currentProfile;
    }

    // Update profile list
    const profileList = document.getElementById("profile-list");
    if (profileList) {
      profileList.innerHTML = "";
      profiles.forEach((profile) => {
        const isActive = profile === currentProfile;
        const profileItem = document.createElement("div");
        profileItem.className = `profile-item ${isActive ? "active" : ""}`;
        profileItem.innerHTML = `
          <div style="display: flex; align-items: center;">
            <span class="profile-item-name">${profile}</span>
            ${
              isActive
                ? '<span class="current-profile-badge">ACTIVE</span>'
                : ""
            }
          </div>
          <div class="profile-item-actions">
            ${
              !isActive
                ? `<button class="profile-btn profile-btn-primary" onclick="switchToProfile('${profile}')">Switch</button>`
                : ""
            }
            ${
              !isActive && profiles.length > 1
                ? `<button class="profile-btn profile-btn-danger" onclick="deleteProfileConfirm('${profile}')">Delete</button>`
                : ""
            }
          </div>
        `;
        profileList.appendChild(profileItem);
      });
    }

    // Update duplicate source dropdown
    const duplicateSelect = document.getElementById("duplicate-source-profile");
    if (duplicateSelect) {
      duplicateSelect.innerHTML = "";
      profiles.forEach((profile) => {
        const option = document.createElement("option");
        option.value = profile;
        option.textContent = profile;
        if (profile === currentProfile) {
          option.selected = true;
        }
        duplicateSelect.appendChild(option);
      });
    }

    // Update export profile dropdown
    const exportSelect = document.getElementById("export-profile-select");
    if (exportSelect) {
      exportSelect.innerHTML = "";
      profiles.forEach((profile) => {
        const option = document.createElement("option");
        option.value = profile;
        option.textContent = profile;
        if (profile === currentProfile) {
          option.selected = true;
        }
        exportSelect.appendChild(option);
      });
    }
  } catch (error) {
    console.error("Error loading profiles:", error);
  }
}

async function switchToProfile(profileName) {
  try {
    const [success, message] = await eel.switchProfile(profileName)();
    if (success) {
      showProfileStatus("create-profile-status", message, "success");

      // Fully refresh GUI like a page reload
      await refreshAllSettings();

      // Reload profile list
      await loadProfileList();
    } else {
      showProfileStatus("create-profile-status", message, "error");
    }
  } catch (error) {
    showProfileStatus("create-profile-status", `Error: ${error}`, "error");
  }
}

// Refresh all settings and GUI elements (like a page refresh)
async function refreshAllSettings() {
  try {
    // Load all settings from the new profile
    const settings = await loadAllSettings();

    // Update all input elements with new settings
    loadInputs(settings);

    // Reload gather tab (field settings)
    const currentGatherTab = document.querySelector(".gather-tab-item.active");
    if (currentGatherTab && typeof switchGatherTab === "function") {
      await switchGatherTab(currentGatherTab);
    } else if (typeof switchGatherTab === "function") {
      // Default to field 1 if no active tab
      const field1Tab = document.getElementById("field-1");
      if (field1Tab) await switchGatherTab(field1Tab);
    }

    // Reload collect tab
    if (typeof loadCollect === "function") {
      await loadCollect();
    }

    // Reload boost tab
    if (typeof loadBoost === "function") {
      loadBoost();
    }

    // Reload kill tab
    if (typeof loadKill === "function") {
      loadKill();
    }

    // Reload quests tab
    if (typeof loadQuests === "function") {
      loadQuests();
    }

    // Reload planters tab
    if (typeof loadPlanters === "function") {
      await loadPlanters();
    }

    // Reload home tasks
    if (typeof loadTasks === "function") {
      await loadTasks();
    }

    // Reload config tab
    if (typeof loadConfig === "function") {
      await loadConfig();
    }

    console.log("All settings refreshed for new profile");
  } catch (error) {
    console.error("Error refreshing settings:", error);
  }
}

async function createNewProfile() {
  const nameInput = document.getElementById("new-profile-name");
  const name = nameInput.value.trim();

  if (!name) {
    showProfileStatus(
      "create-profile-status",
      "Please enter a profile name",
      "error"
    );
    return;
  }

  try {
    const [success, message] = await eel.createProfile(name)();
    if (success) {
      showProfileStatus("create-profile-status", message, "success");
      nameInput.value = "";
      await loadProfileList();
    } else {
      showProfileStatus("create-profile-status", message, "error");
    }
  } catch (error) {
    showProfileStatus("create-profile-status", `Error: ${error}`, "error");
  }
}

async function deleteProfileConfirm(profileName) {
  if (
    confirm(
      `Are you sure you want to delete the profile "${profileName}"? This action cannot be undone.`
    )
  ) {
    try {
      const [success, message] = await eel.deleteProfile(profileName)();
      if (success) {
        showProfileStatus("create-profile-status", message, "success");
        await loadProfileList();
      } else {
        showProfileStatus("create-profile-status", message, "error");
      }
    } catch (error) {
      showProfileStatus("create-profile-status", `Error: ${error}`, "error");
    }
  }
}

async function duplicateExistingProfile() {
  const sourceSelect = document.getElementById("duplicate-source-profile");
  const newNameInput = document.getElementById("duplicate-new-name");

  const sourceName = sourceSelect.value;
  const newName = newNameInput.value.trim();

  if (!newName) {
    showProfileStatus(
      "duplicate-profile-status",
      "Please enter a new profile name",
      "error"
    );
    return;
  }

  try {
    const [success, message] = await eel.duplicateProfile(
      sourceName,
      newName
    )();
    if (success) {
      showProfileStatus("duplicate-profile-status", message, "success");
      newNameInput.value = "";
      await loadProfileList();
    } else {
      showProfileStatus("duplicate-profile-status", message, "error");
    }
  } catch (error) {
    showProfileStatus("duplicate-profile-status", `Error: ${error}`, "error");
  }
}

async function exportProfile() {
  const profileSelect = document.getElementById("export-profile-select");
  const profileName = profileSelect.value;

  if (!profileName) {
    showProfileStatus(
      "export-profile-status",
      "Please select a profile to export",
      "error"
    );
    return;
  }

  try {
    const result = await eel.exportProfile(profileName)();
    const [success, contentOrMessage, filename] = result;

    if (success) {
      // Create download link for the JSON content
      const blob = new Blob([contentOrMessage], { type: "application/json" });
      const url = URL.createObjectURL(blob);

      const a = document.createElement("a");
      a.href = url;
      a.download = filename;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);

      URL.revokeObjectURL(url);

      showProfileStatus(
        "export-profile-status",
        `Profile exported as ${filename}`,
        "success"
      );
    } else {
      showProfileStatus("export-profile-status", contentOrMessage, "error");
    }
  } catch (error) {
    showProfileStatus("export-profile-status", `Error: ${error}`, "error");
  }
}

// Modal functions for import profile
function showImportModal(fileName) {
  const modal = document.getElementById("import-profile-modal");
  const selectedFileSpan = document.getElementById("modal-selected-file");
  const profileNameInput = document.getElementById("modal-profile-name");

  if (modal && selectedFileSpan && profileNameInput) {
    selectedFileSpan.textContent = fileName;
    profileNameInput.value = "imported_profile";
    modal.style.display = "flex";

    // Focus and select the input after modal is shown
    setTimeout(() => {
      profileNameInput.focus();
      profileNameInput.select();

      // Add keyboard event listener for Enter/Escape
      const handleKeyPress = function (e) {
        if (e.key === "Enter") {
          confirmImportProfile();
        } else if (e.key === "Escape") {
          hideImportModal();
        }
      };

      profileNameInput.addEventListener("keydown", handleKeyPress);

      // Store the handler so we can remove it later
      profileNameInput._keyHandler = handleKeyPress;
    }, 100);
  }
}

function hideImportModal() {
  const modal = document.getElementById("import-profile-modal");
  const profileNameInput = document.getElementById("modal-profile-name");
  const fileInput = document.getElementById("import-profile-file");
  const fileNameDisplay = document.getElementById("import-file-name");

  if (modal) {
    modal.style.display = "none";
  }

  // Clean up keyboard event listener
  if (profileNameInput && profileNameInput._keyHandler) {
    profileNameInput.removeEventListener(
      "keydown",
      profileNameInput._keyHandler
    );
    delete profileNameInput._keyHandler;
  }

  // Reset file input and display
  if (fileInput) {
    fileInput.value = "";
    delete fileInput.dataset.selectedFile;
  }

  if (fileNameDisplay) {
    fileNameDisplay.textContent = "No file selected";
  }
}

async function confirmImportProfile() {
  const fileInput = document.getElementById("import-profile-file");
  const profileNameInput = document.getElementById("modal-profile-name");

  if (!fileInput.files || fileInput.files.length === 0) {
    showProfileStatus(
      "import-profile-status",
      "No file selected for import",
      "error"
    );
    hideImportModal();
    return;
  }

  const profileName = profileNameInput.value.trim();
  if (!profileName) {
    alert("Please enter a profile name");
    profileNameInput.focus();
    return;
  }

  const file = fileInput.files[0];

  try {
    // Read file content as text
    const fileContent = await file.text();

    // Import the profile
    const [success, message] = await eel.importProfileContent(
      fileContent,
      profileName
    )();

    if (success) {
      showProfileStatus("import-profile-status", message, "success");
      hideImportModal();
      await loadProfileList();
    } else {
      showProfileStatus("import-profile-status", message, "error");
      // Don't hide modal on error so user can try again
    }
  } catch (error) {
    showProfileStatus("import-profile-status", `Error: ${error}`, "error");
    // Don't hide modal on error
  }
}

// Set up file input event listener (called after HTML is loaded)
function setupFileInputListener() {
  const importFileInput = document.getElementById("import-profile-file");
  if (importFileInput) {
    importFileInput.addEventListener("change", function (e) {
      const fileNameDisplay = document.getElementById("import-file-name");
      console.log("File input changed, files:", e.target.files);

      if (e.target.files && e.target.files.length > 0) {
        const fileName = e.target.files[0].name;
        console.log("Selected file:", fileName);

        // Store the selected file temporarily
        e.target.dataset.selectedFile = fileName;

        // Show the import modal
        showImportModal(fileName);

        console.log("Modal shown for file:", fileName);
      } else {
        console.log("No files selected");
        if (fileNameDisplay) {
          fileNameDisplay.textContent = "No file selected";
        }
        delete e.target.dataset.selectedFile;
      }
    });
    console.log("File input listener set up successfully");
  } else {
    console.error("Could not find import-profile-file element");
  }
}

function showProfileStatus(elementId, message, type) {
  const statusElement = document.getElementById(elementId);
  if (statusElement) {
    statusElement.innerHTML = `<div class="profile-status ${type}">${message}</div>`;
    // Clear status after 5 seconds
    setTimeout(() => {
      statusElement.innerHTML = "";
    }, 5000);
  }
}

// Load profiles tab
$("#profiles-placeholder").load(
  "../htmlImports/tabs/profiles.html",
  loadProfiles
);
