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

function loadDragListOrder(dragListElement, orderArray) {
  if (!orderArray || !Array.isArray(orderArray)) return;

  const container = dragListElement.querySelector(".drag-list-container");
  if (!container) return;

  // Clear existing items
  container.innerHTML = "";

  // Helper function to get category
  function getCategory(taskId) {
    if (taskId.startsWith("gather_")) return "gather";
    if (taskId.startsWith("collect_")) return "collect";
    if (taskId.startsWith("kill_")) return "kill";
    if (taskId.startsWith("quest_")) return "quest";
    return "special";
  }

  // Helper function to get category badge
  function getCategoryBadge(category) {
    const badges = {
      gather: "GATHER",
      collect: "COLLECT",
      kill: "KILL",
      quest: "QUEST",
      special: "SPECIAL",
    };
    return badges[category] || "";
  }

  // Create items in the specified order
  orderArray.forEach((taskId) => {
    let taskName = taskId; // Default to taskId if not found in map

    // Convert task ID to display name
    const displayNames = {
      gather_pine_tree: "Gather: Pine Tree",
      gather_sunflower: "Gather: Sunflower",
      gather_dandelion: "Gather: Dandelion",
      gather_mushroom: "Gather: Mushroom",
      gather_blue_flower: "Gather: Blue Flower",
      gather_clover: "Gather: Clover",
      gather_strawberry: "Gather: Strawberry",
      gather_spider: "Gather: Spider",
      gather_bamboo: "Gather: Bamboo",
      gather_cactus: "Gather: Cactus",
      gather_rose: "Gather: Rose",
      gather_pineapple: "Gather: Pineapple",
      gather_pumpkin: "Gather: Pumpkin",
      gather_coconut: "Gather: Coconut",
      gather_pepper: "Gather: Pepper",
      gather_mountain_top: "Gather: Mountain Top",
      gather_stump: "Gather: Stump",
      collect_wealth_clock: "Collect: Wealth Clock",
      collect_blueberry_dispenser: "Collect: Blueberry Dispenser",
      collect_strawberry_dispenser: "Collect: Strawberry Dispenser",
      collect_coconut_dispenser: "Collect: Coconut Dispenser",
      collect_royal_jelly_dispenser: "Collect: Royal Jelly Dispenser",
      collect_treat_dispenser: "Collect: Treat Dispenser",
      collect_ant_pass_dispenser: "Collect: Ant Pass Dispenser",
      collect_glue_dispenser: "Collect: Glue Dispenser",
      collect_stockings: "Collect: Stockings",
      collect_wreath: "Collect: Wreath",
      collect_feast: "Collect: Feast",
      collect_samovar: "Collect: Samovar",
      collect_snow_machine: "Collect: Snow Machine",
      collect_lid_art: "Collect: Lid Art",
      collect_candles: "Collect: Candles",
      collect_memory_match: "Collect: Memory Match",
      collect_mega_memory_match: "Collect: Mega Memory Match",
      collect_extreme_memory_match: "Collect: Extreme Memory Match",
      collect_winter_memory_match: "Collect: Winter Memory Match",
      collect_honeystorm: "Collect: Honeystorm",
      collect_blue_booster: "Collect: Blue Booster",
      collect_red_booster: "Collect: Red Booster",
      collect_mountain_booster: "Collect: Mountain Booster",
      collect_sticker_stack: "Collect: Sticker Stack",
      collect_sticker_printer: "Collect: Sticker Printer",
      kill_stump_snail: "Kill: Stump Snail",
      kill_ladybug: "Kill: Ladybug",
      kill_rhinobeetle: "Kill: Rhinobeetle",
      kill_scorpion: "Kill: Scorpion",
      kill_mantis: "Kill: Mantis",
      kill_spider: "Kill: Spider",
      kill_werewolf: "Kill: Werewolf",
      kill_coconut_crab: "Kill: Coconut Crab",
      mondo_buff: "Collect: Mondo Buff",
      stinger_hunt: "Stinger Hunt",
      auto_field_boost: "Auto Field Boost",
      ant_challenge: "Ant Challenge",
      quest_polar_bear: "Quest: Polar Bear",
      quest_honey_bee: "Quest: Honey Bee",
      quest_bucko_bee: "Quest: Bucko Bee",
      quest_riley_bee: "Quest: Riley Bee",
      blender: "Blender",
      planters: "Planters",
    };

    if (displayNames[taskId]) {
      taskName = displayNames[taskId];
    }

    const category = getCategory(taskId);
    const badge = getCategoryBadge(category);

    const itemElement = document.createElement("div");
    itemElement.className = "drag-item";
    itemElement.setAttribute("data-id", taskId);
    itemElement.setAttribute("data-category", category);
    itemElement.setAttribute("draggable", "true");
    itemElement.innerHTML = `
      <span class="drag-handle">⋮⋮</span>
      <span class="category-badge">${badge}</span>
      <span class="drag-text">${taskName}</span>
      <div class="drag-actions">
        <button class="drag-action-btn move-to-top" title="Move to top">↑ Top</button>
        <button class="drag-action-btn move-to-bottom" title="Move to bottom">↓ Bottom</button>
      </div>
    `;
    container.appendChild(itemElement);
  });
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
    } else if (ele.className.includes("drag-list")) {
      // Handle drag list elements
      loadDragListOrder(ele, v);
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

/*
=============================================
Image Zoom Functionality
=============================================
*/

let zoomLevel = 1;
let zoomModal = null;
let zoomedImage = null;
let currentImageSrc = null;
let imageContainer = null;
let mouseX = 0;
let mouseY = 0;
let translateX = 0;
let translateY = 0;

function initializeImageZoom() {
  // Create zoom modal if it doesn't exist
  if (!zoomModal) {
    zoomModal = document.createElement("div");
    zoomModal.id = "zoom-modal";
    zoomModal.style.cssText = `
      display: none;
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background-color: rgba(0, 0, 0, 0.9);
      z-index: 10000;
      cursor: zoom-out;
      overflow: hidden;
    `;
    
    imageContainer = document.createElement("div");
    imageContainer.id = "zoom-image-container";
    imageContainer.style.cssText = `
      display: flex;
      justify-content: center;
      align-items: center;
      width: 100%;
      height: 100%;
      position: relative;
      overflow: hidden;
    `;
    
    zoomedImage = document.createElement("img");
    zoomedImage.id = "zoomed-image";
    zoomedImage.style.cssText = `
      max-width: 90vw;
      max-height: 90vh;
      transition: transform 0.1s ease;
      cursor: zoom-in;
      transform-origin: center center;
    `;
    
    const controlsContainer = document.createElement("div");
    controlsContainer.style.cssText = `
      position: fixed;
      top: 2rem;
      right: 2rem;
      display: flex;
      gap: 1rem;
      z-index: 10001;
    `;
    
    const zoomInBtn = document.createElement("button");
    zoomInBtn.textContent = "+";
    zoomInBtn.className = "zoom-control-btn";
    zoomInBtn.onclick = (e) => {
      e.stopPropagation();
      zoomImageCentered(1.2);
    };
    
    const zoomOutBtn = document.createElement("button");
    zoomOutBtn.textContent = "-";
    zoomOutBtn.className = "zoom-control-btn";
    zoomOutBtn.onclick = (e) => {
      e.stopPropagation();
      zoomImageCentered(0.8);
    };
    
    const resetBtn = document.createElement("button");
    resetBtn.textContent = "Reset";
    resetBtn.className = "zoom-control-btn";
    resetBtn.onclick = (e) => {
      e.stopPropagation();
      resetZoom();
    };
    
    const closeBtn = document.createElement("button");
    closeBtn.textContent = "×";
    closeBtn.className = "zoom-control-btn";
    closeBtn.style.fontSize = "2rem";
    closeBtn.onclick = (e) => {
      e.stopPropagation();
      closeZoomModal();
    };
    
    controlsContainer.appendChild(zoomInBtn);
    controlsContainer.appendChild(zoomOutBtn);
    controlsContainer.appendChild(resetBtn);
    controlsContainer.appendChild(closeBtn);
    
    imageContainer.appendChild(zoomedImage);
    zoomModal.appendChild(imageContainer);
    zoomModal.appendChild(controlsContainer);
    
    // Track mouse position for scroll wheel zoom
    imageContainer.addEventListener("mousemove", (e) => {
      const rect = imageContainer.getBoundingClientRect();
      mouseX = e.clientX - rect.left;
      mouseY = e.clientY - rect.top;
    });
    
    // Scroll wheel zoom (mouse position based)
    imageContainer.addEventListener("wheel", (e) => {
      e.preventDefault();
      e.stopPropagation();
      const delta = e.deltaY > 0 ? 0.9 : 1.1;
      zoomImageAtMouse(delta, e.clientX, e.clientY);
    });
    
    // Close on background click
    zoomModal.onclick = (e) => {
      if (e.target === zoomModal) {
        closeZoomModal();
      }
    };
    
    // Close on Escape key
    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape" && zoomModal.style.display === "block") {
        closeZoomModal();
      }
    });
    
    document.body.appendChild(zoomModal);
  }
  
  // Add click handlers to all zoomable images
  document.addEventListener("click", (e) => {
    if (e.target.classList.contains("zoomable-image")) {
      e.preventDefault();
      e.stopPropagation();
      openZoomModal(e.target.src);
    }
  });
}

function openZoomModal(imageSrc) {
  if (!zoomModal) {
    initializeImageZoom();
  }
  currentImageSrc = imageSrc;
  zoomedImage.src = imageSrc;
  zoomLevel = 1;
  translateX = 0;
  translateY = 0;
  zoomedImage.style.transform = `translate(${translateX}px, ${translateY}px) scale(${zoomLevel})`;
  zoomModal.style.display = "block";
  document.body.style.overflow = "hidden";
  
  // Reset transform origin to center
  zoomedImage.style.transformOrigin = "center center";
}

function closeZoomModal() {
  if (zoomModal) {
    zoomModal.style.display = "none";
    document.body.style.overflow = "";
    zoomLevel = 1;
    translateX = 0;
    translateY = 0;
  }
}

function zoomImageAtMouse(factor, clientX, clientY) {
  const rect = imageContainer.getBoundingClientRect();
  const containerCenterX = rect.left + rect.width / 2;
  const containerCenterY = rect.top + rect.height / 2;
  
  // Get mouse position relative to container center
  const mouseOffsetX = clientX - containerCenterX;
  const mouseOffsetY = clientY - containerCenterY;
  
  // Calculate new zoom level
  const newZoomLevel = zoomLevel * factor;
  const clampedZoom = Math.max(0.5, Math.min(newZoomLevel, 5));
  
  if (clampedZoom === zoomLevel) return; // No change if at limits
  
  // Calculate the zoom point relative to the image center
  // We need to adjust translate to keep the point under the mouse fixed
  const zoomRatio = clampedZoom / zoomLevel;
  
  // Adjust translate to zoom towards mouse position
  translateX = translateX * zoomRatio - mouseOffsetX * (zoomRatio - 1);
  translateY = translateY * zoomRatio - mouseOffsetY * (zoomRatio - 1);
  
  zoomLevel = clampedZoom;
  updateImageTransform();
}

function zoomImageCentered(factor) {
  const newZoomLevel = zoomLevel * factor;
  zoomLevel = Math.max(0.5, Math.min(newZoomLevel, 5));
  
  // For centered zoom, reset translate
  translateX = 0;
  translateY = 0;
  zoomedImage.style.transformOrigin = "center center";
  updateImageTransform();
}

function updateImageTransform() {
  zoomedImage.style.transform = `translate(${translateX}px, ${translateY}px) scale(${zoomLevel})`;
}

function resetZoom() {
  zoomLevel = 1;
  translateX = 0;
  translateY = 0;
  zoomedImage.style.transformOrigin = "center center";
  updateImageTransform();
}

// Initialize zoom when DOM is ready
if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", initializeImageZoom);
} else {
  initializeImageZoom();
}

// Re-initialize when new content is loaded (for dynamically loaded tabs)
// Use MutationObserver to detect when new images are added
const observer = new MutationObserver((mutations) => {
  mutations.forEach((mutation) => {
    mutation.addedNodes.forEach((node) => {
      if (node.nodeType === 1) { // Element node
        // Check if the node or its children contain zoomable images
        if (node.classList && node.classList.contains("zoomable-image")) {
          // Image is already set up by event delegation
        } else if (node.querySelectorAll) {
          const images = node.querySelectorAll(".zoomable-image");
          // Images will be handled by event delegation
        }
      }
    });
  });
});

// Start observing the document body for changes
observer.observe(document.body, {
  childList: true,
  subtree: true
});
