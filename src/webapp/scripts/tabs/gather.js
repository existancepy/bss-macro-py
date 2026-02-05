/*
=============================================
Gather Tab
=============================================
*/
var fieldNo = 1;
//save the enabled status for the fields
async function saveEnabled() {
  const fields = (await loadSettings()).fields;
  fields[fieldNo - 1] = ele.value;
  eel.saveProfileSetting("fields", fields);
}
function saveField() {
  const fieldProperties = [
    "shift_lock",
    "field_drift_compensation",
    "shape",
    "size",
    "width",
    "invert_lr",
    "invert_fb",
    "turn",
    "turn_times",
    "mins",
    "backpack",
    "return",
    "start_location",
    "distance",
    "goo",
    "goo_interval",
  ];

  // Validate goo_interval minimum value
  const gooIntervalElement = document.getElementById("goo_interval");
  if (gooIntervalElement && gooIntervalElement.value) {
    const value = parseInt(gooIntervalElement.value);
    if (value < 3) {
      gooIntervalElement.value = 3;
    }
  }

  const fieldData = generateSettingObject(fieldProperties);
  eel.saveField(getInputValue("field"), fieldData);
}
//save the fields_enabled
async function updateFieldEnable(ele) {
  //save
  const fields_enabled = (await loadSettings()).fields_enabled;
  fields_enabled[fieldNo - 1] = ele.checked;
  eel.saveProfileSetting("fields_enabled", fields_enabled);
}

//load the field selected in the dropdown
async function loadAndSaveField(ele) {
  const data = (await eel.loadFields()())[getDropdownValue(ele)];
  loadInputs(data);
  //save
  const fields = (await loadSettings()).fields;
  fields[fieldNo - 1] = getDropdownValue(ele);
  eel.saveProfileSetting("fields", fields);
}

async function switchGatherTab(target) {
  fieldNo = target.id.split("-")[1];
  //remove the arrow indicator
  const selector = document.getElementById("gather-select");
  if (selector) selector.remove();
  Array.from(document.getElementsByClassName("gather-tab-item")).forEach((x) =>
    x.classList.remove("active")
  ); //remove the active class
  //add indicator + active class
  target.classList.add("active");
  target.innerHTML =
    `<div class = "select-indicator" id = "gather-select"></div>` +
    target.innerHTML;
  document.getElementById("gather-field").innerText = `Gather Field ${fieldNo}`;
  //scroll back to top
  document.getElementById("gather").scrollTo(0, 0);
  //load the fields
  const settings = await loadSettings();
  const fieldDropdown = document.getElementById("field");
  setDropdownValue(fieldDropdown, settings.fields[fieldNo - 1]);
  document.getElementById("field_enable").checked =
    settings.fields_enabled[fieldNo - 1];
  //get the pattern list
  const patterns = await eel.getPatterns()();
  setDropdownData("shape", patterns);
  //load the inputs
  loadAndSaveField(fieldDropdown);
}

$("#gather-placeholder")
  .load("../htmlImports/tabs/gather.html", () =>
    switchGatherTab(document.getElementById("field-1"))
  ) //load home tab, switch to field 1 once its done loading
  .on("click", ".gather-tab-item", (event) =>
    switchGatherTab(event.currentTarget)
  ) //navigate between fields
  .on("click", "#reset-field-button", async (event) => {
    event.preventDefault();

    // Get the currently selected field name
    const fieldDropdown = document.getElementById("field");
    const currentFieldName = getDropdownValue(fieldDropdown);

    if (!currentFieldName) {
      alert("Please select a field first.");
      return;
    }

    // Show confirmation dialog
    const confirmReset = confirm(
      `Are you sure you want to reset "${currentFieldName}" field settings to default values? This action cannot be undone.`
    );

    if (!confirmReset) {
      return;
    }

    try {
      // Call the reset function
      const success = await eel.resetFieldToDefault(currentFieldName)();

      if (success) {
        // Reload the field data and update the UI
        const data = (await eel.loadFields()())[currentFieldName];
        loadInputs(data);
        alert(
          `Successfully reset "${currentFieldName}" field settings to defaults.`
        );
      } else {
        alert(
          `Failed to reset "${currentFieldName}" field settings. Field may not exist in default settings.`
        );
      }
    } catch (error) {
      console.error("Error resetting field:", error);
      alert("An error occurred while resetting field settings.");
    }
  })
  .on("click", "#export-field-button", async (event) => {
    event.preventDefault();

    // Get the currently selected field name
    const fieldDropdown = document.getElementById("field");
    const currentFieldName = getDropdownValue(fieldDropdown);

    if (!currentFieldName) {
      alert("Please select a field first.");
      return;
    }

    try {
      // Call the export function
      const jsonSettings = await eel.exportFieldSettings(currentFieldName)();

      if (jsonSettings) {
        // Parse JSON to extract metadata
        let metadata = {};
        try {
          const parsedData = JSON.parse(jsonSettings);
          metadata = parsedData.metadata || {};
        } catch (e) {
          // If parsing fails, that's okay - just use empty metadata
        }

        // Copy to clipboard
        await navigator.clipboard.writeText(jsonSettings);
        
        // Build success message with metadata
        let successMsg = `Settings for "${currentFieldName}" exported and copied to clipboard!`;
        if (metadata.macro_version) {
          successMsg += `\n\nExport details:\nMacro version: ${metadata.macro_version}`;
        }
        if (metadata.export_date) {
          successMsg += `\nExported: ${new Date(metadata.export_date).toLocaleString()}`;
        }
        
        alert(successMsg);
      } else {
        alert("Failed to export field settings. Field may not exist.");
      }
    } catch (error) {
      console.error("Error exporting field settings:", error);
      alert("An error occurred while exporting field settings.");
    }
  })
  .on("click", "#import-field-button", async (event) => {
    event.preventDefault();

    // Get the currently selected field name
    const fieldDropdown = document.getElementById("field");
    const currentFieldName = getDropdownValue(fieldDropdown);

    if (!currentFieldName) {
      alert("Please select a field first.");
      return;
    }

    // Show the import modal
    const modal = document.getElementById("import-modal");
    const textarea = document.getElementById("import-json-textarea");
    textarea.value = "";
    modal.style.display = "flex";
  })
  .on("click", "#cancel-import-button", (event) => {
    event.preventDefault();
    // Hide the import modal
    document.getElementById("import-modal").style.display = "none";
  })
  .on("click", "#confirm-import-button", async (event) => {
    event.preventDefault();

    const fieldDropdown = document.getElementById("field");
    const currentFieldName = getDropdownValue(fieldDropdown);
    const textarea = document.getElementById("import-json-textarea");
    const jsonSettings = textarea.value.trim();

    if (!jsonSettings) {
      alert("Please paste JSON settings to import.");
      return;
    }

    try {
      // Call the import function
      const result = await eel.importFieldSettings(currentFieldName, jsonSettings)();

      if (result && result.success) {
        // Reload the field data and update the UI
        const data = (await eel.loadFields()())[currentFieldName];
        loadInputs(data);
        // Hide the modal
        document.getElementById("import-modal").style.display = "none";

        // Build success message with metadata
        let successMsg = `Successfully imported settings for "${currentFieldName}"!`;
        
        // Add metadata information if available
        if (result.imported_from_field && result.imported_from_field !== "unknown") {
          successMsg += `\n\nImported from field: ${result.imported_from_field}`;
        }
        if (result.macro_version && result.macro_version !== "unknown") {
          successMsg += `\nMacro version: ${result.macro_version}`;
        }
        
        // Add pattern replacement information
        if (result.missing_patterns && result.missing_patterns.length > 0) {
          const patternMsg = result.missing_patterns.join(", ");
          successMsg += `\n\nNote: Some patterns were not found and were replaced:\n${patternMsg}`;
        }
        
        alert(successMsg);
      } else {
        alert("Failed to import field settings. Please check your JSON format.");
      }
    } catch (error) {
      console.error("Error importing field settings:", error);
      alert("An error occurred while importing field settings. Please check your JSON format.");
    }
  })
  .on("click", "#import-modal", function(event) {
    // Close modal when clicking outside the modal content
    if (event.target === this) {
      $(this).hide();
    }
  });
