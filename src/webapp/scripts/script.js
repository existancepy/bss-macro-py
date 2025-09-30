//change the styling of the purple buttons
//element: the purple button element
//label: the text labels of the button [not-active-label, active-label]
function purpleButtonToggle(element, labels) {
  //check for active class
  if (element.classList.contains("active")) {
    element.innerText = labels[0];
    element.classList.remove("active");
    return labels[1];
  }

  element.innerText = labels[1];
  element.classList.add("active");
  return labels[0];
}

//get the value of input elements like checkboxes, dropdown and textboxes
function getInputValue(id) {
  const ele = document.getElementById(id);
  if (!ele) {
    console.error("Element not found:", id);
    return "";
  }
  //checkbox
  if (ele.tagName == "INPUT" && ele.type == "checkbox") {
    return ele.checked;
    //textbox
  } else if (ele.tagName == "INPUT" && ele.type == "text") {
    const value = ele.value;
    if (
      !value &&
      (ele.dataset.inputType == "float" || ele.dataset.inputType == "int")
    )
      return 0;
    if (!value) return "";
    return value;
    //custom dropdown
  } else if (ele.tagName == "DIV" && ele.className.includes("custom-select")) {
    return getDropdownValue(ele).toLowerCase();
    //slider
  } else if (ele.tagName == "INPUT" && ele.type == "range") {
    return ele.value;
    //keybind
  } else if (ele.tagName == "DIV" && ele.className.includes("keybind-input")) {
    return ele.dataset.keybind || "";
  }
}

async function loadSettings() {
  return await eel.loadSettings()();
}

async function loadAllSettings() {
  return await eel.loadAllSettings()();
}
//save the setting
//element
//type: setting type, eg: profile, general
function saveSetting(ele, type) {
  //apply element binding (only for checkboxes)
  if (ele.dataset && ele.dataset.inputBind) {
    const bindTargetId = ele.dataset.inputBind;
    const bindTarget = document.getElementById(bindTargetId);
    if (ele.checked) {
      bindTarget.checked = false;
      eel.saveProfileSetting(bindTargetId, false);
    }
  }
  const id = ele.id;
  const value = getInputValue(id);

  if (type == "profile") {
    eel.saveProfileSetting(id, value);
  } else if (type == "general") {
    eel.saveGeneralSetting(id, value);
  }
}

//returns a object based on the settings
//proprties: an array of property names
//note: element corresponding to the property must have the same id as that property
function generateSettingObject(properties) {
  let out = {};
  properties.forEach((x) => {
    out[x] = getInputValue(x);
  });
  return out;
}

//load fields based on the obj data
eel.expose(loadInputs);
function loadInputs(obj, save = "") {
  for (const [k, v] of Object.entries(obj)) {
    const ele = document.getElementById(k);
    //check if element exists
    if (!ele) continue;
    if (ele.type == "checkbox") {
      ele.checked = v;
    } else if (ele.className.includes("custom-select")) {
      setDropdownValue(ele, v);
    } else if (ele.className.includes("keybind-input")) {
      // Handle keybind elements
      ele.dataset.keybind = v;
      const displayText = v ? v.replace(/\+/g, " + ") : "Click to record";
      ele.querySelector(".keybind-display").textContent = displayText;
    } else {
      ele.value = v;
    }
  }
  if (save == "profile") {
    eel.saveDictProfileSettings(obj);
  }
}

/*
=============================================
Header
=============================================
*/
//load the html
$("#header-placeholder").load("../htmlImports/persistent/header.html");

/*
=============================================
Utils
=============================================
*/

//utility to run after content has loaded
//to be fired as a callback in ajax .load
function textboxRestriction(ele, evt) {
  var charCode = evt.which ? evt.which : evt.keyCode;
  if (ele.dataset.inputLimit != 0 && ele.value.length >= ele.dataset.inputLimit)
    return false;
  if (ele.dataset.inputType == "float") {
    if (charCode == 46) {
      //Check if the text already contains the . character
      if (ele.value.indexOf(".") === -1) {
        return true;
      } else {
        return false;
      }
    } else {
      if (charCode > 31 && (charCode < 48 || charCode > 57)) return false;
    }
    return true;
  } else if (ele.dataset.inputType == "int") {
    return !(charCode > 31 && (charCode < 48 || charCode > 57));
  }
}

//disable browser actions
/*
window.oncontextmenu = function(event) {
    // block right-click / context-menu
    event.preventDefault();
    event.stopPropagation();
    return false;
};
*/
// Function to check if current key combination matches a configured keybind
function isConfiguredKeybind(event) {
  // Get current keybinds from settings
  const startKeybind =
    document.getElementById("start_keybind")?.dataset.keybind;
  const stopKeybind = document.getElementById("stop_keybind")?.dataset.keybind;

  if (!startKeybind && !stopKeybind) return false;

  // Build current key combination
  let currentCombo = [];
  if (event.ctrlKey) currentCombo.push("Ctrl");
  if (event.altKey) currentCombo.push("Alt");
  if (event.shiftKey) currentCombo.push("Shift");
  if (event.metaKey) currentCombo.push("Cmd");

  // Add the main key
  let mainKey = event.key;
  if (mainKey === " ") mainKey = "Space";
  else if (mainKey === "Control") mainKey = "Ctrl";
  else if (mainKey === "Alt") mainKey = "Alt";
  else if (mainKey === "Shift") mainKey = "Shift";
  else if (mainKey === "Meta") mainKey = "Cmd";
  else if (mainKey.startsWith("F") && mainKey.length <= 3) {
    // Function keys (F1, F2, etc.)
    mainKey = mainKey;
  } else if (mainKey.length === 1) {
    // Regular character keys
    mainKey = mainKey.toUpperCase();
  }

  currentCombo.push(mainKey);
  const currentComboString = currentCombo.join("+");

  // Check if it matches either configured keybind
  return (
    currentComboString === startKeybind || currentComboString === stopKeybind
  );
}

window.addEventListener("keydown", (event) => {
  const key = event.key;
  const disabledKeys = ["F5", "F12"];

  // Block specific browser shortcuts that don't interfere with macro
  if (disabledKeys.includes(key)) {
    event.preventDefault();
    event.stopPropagation();
    return false;
  } else if (event.ctrlKey && event.shiftKey && event.key == "I") {
    // block Strg+Shift+I (DevTools)
    event.preventDefault();
    event.stopPropagation();
    return false;
  } else if (event.ctrlKey && event.shiftKey && event.key == "J") {
    // block Strg+Shift+J (Console)
    event.preventDefault();
    event.stopPropagation();
    return false;
  }

  // Block ALL configured keybinds to prevent browser interference
  if (isConfiguredKeybind(event)) {
    event.preventDefault();
    event.stopPropagation();
    return false;
  }
});

/*
=============================================
Custom Select
=============================================
*/
dropdownOpen = false;
//pass an optionEle to set the select-area
function updateDropDownDisplay(optionEle) {
  const parentEle = optionEle.parentElement.parentElement.parentElement;
  //set the data-value attribute of the select
  const selectEle = parentEle.children[0].children[0];
  selectEle.dataset.value = optionEle.dataset.value;
  //set the display to match the option
  selectEle.innerHTML = optionEle.innerHTML;
}
//document click event
function dropdownClicked(event) {
  //get the element that was clicked
  const ele = event.target;
  if (!ele) {
    dropdownOpen = false;
    return;
  }
  //toggle dropdown
  if (ele.className.includes("select-area")) {
    //get the associated custom-select parent element
    const parent = ele.parentElement;
    const optionsEle = parent.children[1].children[0];
    closeAllDropdowns(optionsEle); //close all other dropdowns
    //toggle the dropdown menu
    if (dropdownOpen !== optionsEle) {
      //open it
      dropdownOpen = optionsEle;
      optionsEle.style.display = "block";
      const currValue = parent.children[0].children[0].dataset.value;
      //highlight the corresponding value option
      //ie if the value of the dropdown is "none", highlight the "none option"
      Array.from(optionsEle.children).forEach((x) => {
        x.dataset.value == currValue
          ? x.classList.add("selected")
          : x.classList.remove("selected");
      });
      //check if its going below the screen and render the menu above
      parent.style.transform = "none";
      optionsEle.style.transform = "none";
      ele.style.transform = "none";
      const height = optionsEle.getBoundingClientRect().height;
      const y = optionsEle.getBoundingClientRect().top;
      //check if it goes below the screen
      //if it is flipped and goes above the screen, prioritise rendering the dropdown down
      if (height + y > window.innerHeight && y > height) {
        parent.style.transform = "rotate(180deg)"; //render the dropdown menu above
        //flip everything to face the correct direction
        optionsEle.style.transform = "rotate(180deg)";
        ele.style.transform = "rotate(180deg)";
      }
    } else {
      //close it
      optionsEle.style.display = "none";
      dropdownOpen = false;
    }
  } else {
    //close all dropdowns, because an option was selected or the user clicked elsewhere
    closeAllDropdowns();
    if (ele.className.includes("option")) {
      updateDropDownDisplay(ele);
      const parentEle = ele.parentElement.parentElement.parentElement;
      let funcParams = parentEle.dataset.onchange.replace("this", "parentEle");
      eval(funcParams);
      dropdownOpen = false;
    } else {
      //try again, but with the parent element
      //this creates a recursive loop to account for children elements (could be expensive)
      dropdownClicked({ target: ele.parentElement });
    }
  }
}

function getDropdownValue(ele) {
  return ele.children[0].children[0].dataset.value;
}

function setDropdownValue(ele, value) {
  const optionsEle = ele.children[1].children[0];
  for (let i = 0; i < optionsEle.children.length; i++) {
    const x = optionsEle.children[i];
    if (x.dataset.value == value) {
      updateDropDownDisplay(x);
      break;
    }
  }
}
//close all other dropdown menus
//if ele is undefined, close all menus
function closeAllDropdowns(ele) {
  Array.from(document.getElementsByClassName("select-menu")).forEach((x) => {
    if (ele !== x) x.style.display = "none";
  });
}
function dropdownHover(event) {
  const ele = event.target;
  if (ele.className.includes("option")) {
    Array.from(document.getElementsByClassName("option")).forEach((x) => {
      x.classList.remove("selected");
    });
    ele.classList.add("selected");
  }
}
document.addEventListener("click", dropdownClicked);
document.addEventListener("mouseover", dropdownHover);

// Keybind recording functionality
let keybindRecording = false;
let currentKeybindElement = null;
let keybindSequence = [];

function startKeybindRecording(elementId) {
  const element = document.getElementById(elementId);
  if (keybindRecording) {
    stopKeybindRecording();
    return;
  }

  keybindRecording = true;
  currentKeybindElement = element;
  element.dataset.recording = "true";
  element.style.borderColor = "#3E74DF";
  element.style.backgroundColor = "#36393F";
  element.style.boxShadow = "0 0 10px rgba(62, 116, 223, 0.3)";
  element.querySelector(".keybind-display").textContent =
    "Press key combination...";

  // Reset sequence
  keybindSequence = [];

  // Add event listeners for key recording
  document.addEventListener("keydown", handleKeybindKeyDown);
  document.addEventListener("keyup", handleKeybindKeyUp);

  // Add click listener to stop recording if user clicks elsewhere
  setTimeout(() => {
    document.addEventListener("click", handleKeybindClickOutside);
  }, 100);
}

function handleKeybindClickOutside(event) {
  if (
    keybindRecording &&
    currentKeybindElement &&
    !currentKeybindElement.contains(event.target)
  ) {
    stopKeybindRecording();
  }
}

// Function to update all keybind displays in real time
async function updateKeybindDisplay() {
  try {
    // Update start button text using the existing function from home.js
    if (typeof updateStartButtonText === "function") {
      await updateStartButtonText();
    }

    // Also update the button text directly as fallback
    const settings = await loadAllSettings();
    const startKey = settings.start_keybind || "F1";
    const stopKey = settings.stop_keybind || "F3";

    const startButton = document.getElementById("start-btn");
    if (startButton) {
      startButton.textContent = `Start [${startKey}]`;
    }

    // Update keybind input field displays
    const startKeybindElement = document.getElementById("start_keybind");
    const stopKeybindElement = document.getElementById("stop_keybind");

    if (
      startKeybindElement &&
      startKeybindElement.querySelector(".keybind-display")
    ) {
      startKeybindElement.querySelector(".keybind-display").textContent =
        startKey.replace(/\+/g, " + ");
    }

    if (
      stopKeybindElement &&
      stopKeybindElement.querySelector(".keybind-display")
    ) {
      stopKeybindElement.querySelector(".keybind-display").textContent =
        stopKey.replace(/\+/g, " + ");
    }
  } catch (error) {
    // Silently handle errors
  }
}

function stopKeybindRecording() {
  if (!keybindRecording) return;

  keybindRecording = false;
  if (currentKeybindElement) {
    currentKeybindElement.dataset.recording = "false";
    currentKeybindElement.style.borderColor = "#7A77BB";
    currentKeybindElement.style.backgroundColor = "#2F3136";
    currentKeybindElement.style.boxShadow = "none";
  }
  currentKeybindElement = null;
  keybindSequence = [];

  // Remove event listeners
  document.removeEventListener("keydown", handleKeybindKeyDown);
  document.removeEventListener("keyup", handleKeybindKeyUp);
  document.removeEventListener("click", handleKeybindClickOutside);
}

function handleKeybindKeyDown(event) {
  if (!keybindRecording || !currentKeybindElement) return;

  event.preventDefault();
  event.stopPropagation();

  // Get the key name
  let keyName = event.key;

  // Handle special keys
  if (event.key === " ") {
    keyName = "Space";
  } else if (event.key === "Control") {
    keyName = "Ctrl";
  } else if (event.key === "Alt") {
    keyName = "Alt";
  } else if (event.key === "Shift") {
    keyName = "Shift";
  } else if (event.key === "Meta") {
    keyName = "Cmd";
  } else if (event.key.startsWith("F") && event.key.length <= 3) {
    // Function keys (F1, F2, etc.)
    keyName = event.key;
  } else if (event.key.length === 1) {
    // Regular character keys
    keyName = event.key.toUpperCase();
  }

  // Add to sequence if not already present
  if (!keybindSequence.includes(keyName)) {
    keybindSequence.push(keyName);
  }

  // Update display
  const displayText = keybindSequence.join(" + ");
  currentKeybindElement.querySelector(".keybind-display").textContent =
    displayText;
}

function finalizeKeybind() {
  if (!keybindRecording || !currentKeybindElement) return;

  // Save the keybind combination
  const keybindString = keybindSequence.join("+");
  currentKeybindElement.dataset.keybind = keybindString;

  // Update the display to show the saved keybind
  const displayText = keybindString.replace(/\+/g, " + ");
  currentKeybindElement.querySelector(".keybind-display").textContent =
    displayText;

  // Trigger the save function
  const triggerFunction = currentKeybindElement.getAttribute(
    "data-trigger-function"
  );
  if (triggerFunction) {
    try {
      // Replace 'this' with the actual element reference
      const functionCall = triggerFunction.replace(
        "this",
        "currentKeybindElement"
      );
      eval(functionCall);

      // Update UI elements in real time
      updateKeybindDisplay();
    } catch (error) {
      // Silently handle errors
    }
  }

  // Stop recording
  stopKeybindRecording();
}

function handleKeybindKeyUp(event) {
  if (!keybindRecording || !currentKeybindElement) return;

  event.preventDefault();
  event.stopPropagation();

  // Finalize the keybind when any key is released
  finalizeKeybind();
}
