/*
=============================================
Home Tab
=============================================
*/

//use a python function to open the link in the user's actual browser
function ahref(link) {
  eel.openLink(link);
}

//update the button text with current keybinds and state
async function updateStartButtonText() {
  const settings = await loadAllSettings();
  const startKey = settings.start_keybind || "F1";
  const stopKey = settings.stop_keybind || "F3";
  // const pauseKey = settings.pause_keybind || "F2";

  // Check current run state
  try {
    const runState = await eel.getRunState()();
    // 2 = running, 3 = stopped, 6 = paused

    const startBtn = document.getElementById("start-btn");
    const stopBtn = document.getElementById("stop-btn");
    // const pauseBtn = document.getElementById("pause-btn");

    if (runState === 2) {
      // Running: show Stop button
      if (startBtn) startBtn.style.display = "none";
      if (stopBtn) {
        stopBtn.style.display = "block";
        stopBtn.textContent = `Stop [${stopKey}]`;
      }
    } else {
      // Stopped or Paused: show Start button only
      if (startBtn) {
        startBtn.style.display = "block";
        startBtn.classList.remove("active");
        startBtn.disabled = false;
        startBtn.textContent = `Start [${startKey}]`;
      }
      if (stopBtn) stopBtn.style.display = "none";
    }
  } catch (error) {
    // Fallback to just showing start button
    const startBtn = document.getElementById("start-btn");
    if (startBtn) {
      startBtn.style.display = "block";
      startBtn.disabled = false;
      startBtn.textContent = `Start [${startKey}]`;
    }
  }
}

//toggle the start/stop/pause button visuals based on run state
eel.expose(toggleStartStop);
async function toggleStartStop() {
  const settings = await loadAllSettings();
  const startKey = settings.start_keybind || "F1";
  const stopKey = settings.stop_keybind || "F3";
  // const pauseKey = settings.pause_keybind || "F2";

  // Check current run state
  try {
    const runState = await eel.getRunState()();
    // 2 = running, 3 = stopped, 6 = paused

    const startBtn = document.getElementById("start-btn");
    const stopBtn = document.getElementById("stop-btn");
    // const pauseBtn = document.getElementById("pause-btn");

    if (runState === 2) {
      // Running: show Stop button
      if (startBtn) startBtn.style.display = "none";
      if (stopBtn) {
        stopBtn.style.display = "block";
        stopBtn.textContent = `Stop [${stopKey}]`;
      }
    } else {
      // Stopped or Paused: show Start button only
      if (startBtn) {
        startBtn.style.display = "block";
        startBtn.classList.remove("active");
        startBtn.disabled = false;
        startBtn.textContent = `Start [${startKey}]`;
      }
      if (stopBtn) stopBtn.style.display = "none";
    }

    return true; // Success
  } catch (error) {
    return false;
  }
}

eel.expose(log);
function log(time = "", msg = "", color = "") {
  document.getElementById("log");
  let timeText = "";
  if (time) timeText = `[${time}]`;
  const html = `
    <div class = "log-msg"><span style="background-color: #${color}; align-self: start"></span>${timeText} ${msg}</div>
    `;
  const logs = document.getElementById("logs");
  logs.innerHTML += html;
  logs.scrollTop = logs.scrollHeight;
}

//returns a html string for the task
function taskHTML(title, desc = "") {
  const html = `
    <div style="margin-top: 1rem;">
        <div style="font-size: 1.1rem;">${title}</div>
        <div style="font-size: 0.9rem; color: #ADB5BD; display:flex; align-items:center;">${
          desc.includes("<img") ? desc : toTitleCase(desc)
        }</div>
        <div style="background-color: #949393; height: 1px; width: 95%; margin-top: 0.4rem;"></div>
    </div>
    `;
  return html;
}

function secondsToMinsAndHours(time) {
  if (time < 0) return "Ready!";
  const hours = Math.floor(time / 3600);
  const minutes = Math.floor((time - hours * 3600) / 60);
  return `${hours}h ${minutes}m`;
}

//load the tasks
//also set max-height for logs
eel.expose(loadTasks);
// Prevent updates while user is actively changing the dropdown
let isUserChangingMode = false;
let modeUpdateTimeout = null;

eel.expose(updateMacroMode);
async function updateMacroMode() {
  // Don't update if user is currently changing the dropdown
  if (isUserChangingMode) {
    return;
  }

  // Clear any pending updates
  if (modeUpdateTimeout) {
    clearTimeout(modeUpdateTimeout);
  }

  // Debounce updates to prevent flashing
  modeUpdateTimeout = setTimeout(async () => {
    const settings = await loadAllSettings();
    const macroModeDropdown = document.getElementById("macro_mode");
    if (macroModeDropdown && !isUserChangingMode) {
      const currentValue = settings.macro_mode || "normal";

      // Only update if the value actually differs to prevent unnecessary DOM updates
      if (macroModeDropdown.value !== currentValue) {
        macroModeDropdown.value = currentValue;
      }
    }
  }, 50);
}

async function loadTasks() {
  const setdat = await loadAllSettings();
  let out = "";

  // Update macro mode dropdown to match current settings (only if user is not actively changing it)
  const macroModeDropdown = document.getElementById("macro_mode");
  if (macroModeDropdown && !isUserChangingMode) {
    const currentValue = setdat.macro_mode || "normal";

    if (macroModeDropdown.value !== currentValue) {
      macroModeDropdown.value = currentValue;
    }
  }

  // Check if field-only mode is enabled
  if (setdat.macro_mode === "field") {
    out += taskHTML("Field Only Mode", "🌾 Gathering in fields only");

    // Get priority order and filter to only include gather tasks for enabled fields
    const priorityOrder = setdat.task_priority_order || [];
    const fieldOnlyTasks = [];

    // Filter priority order to only include gather tasks for enabled fields
    for (const taskId of priorityOrder) {
      if (taskId.startsWith("gather_")) {
        const fieldName = taskId.replace("gather_", "").replace("_", " ");
        // Check if this field is enabled
        for (let i = 0; i < setdat.fields_enabled.length; i++) {
          if (setdat.fields_enabled[i] && setdat.fields[i] === fieldName) {
            fieldOnlyTasks.push(taskId);
            break;
          }
        }
      }
    }

    // If no gather tasks are in priority order, fall back to sequential order of enabled fields
    if (fieldOnlyTasks.length === 0) {
      for (let i = 0; i < setdat.fields_enabled.length; i++) {
        if (setdat.fields_enabled[i]) {
          const field = setdat.fields[i];
          fieldOnlyTasks.push(`gather_${field.replaceAll(" ", "_")}`);
        }
      }
    }

    // Display gather tasks in priority order
    let gatherIndex = 1;
    for (const taskId of fieldOnlyTasks) {
      const fieldName = taskId.replace("gather_", "").replace("_", " ");
      out += taskHTML(
        `Gather ${gatherIndex}`,
        `${fieldEmojis[fieldName.replaceAll(" ", "_")]} ${fieldName}`
      );
      gatherIndex++;
    }

    // Display the tasks
    document.getElementById("task-list").innerHTML = out;
    return;
  }

  // Check if quest mode is enabled
  if (setdat.macro_mode === "quest") {
    out += taskHTML("Quest Mode", "📜 Doing quests only");

    // Add quest tasks that are enabled
    const questTasks = [
      { key: "honey_bee_quest", name: "Honey Bee Quest", emoji: "🐝" },
      { key: "bucko_bee_quest", name: "Bucko Bee Quest", emoji: "🏴‍☠️" },
      { key: "riley_bee_quest", name: "Riley Bee Quest", emoji: "🎸" },
      { key: "polar_bear_quest", name: "Polar Bear Quest", emoji: "🐻" },
    ];

    for (const quest of questTasks) {
      if (setdat[quest.key]) {
        out += taskHTML(quest.name, `${quest.emoji} ${quest.name}`);
      }
    }

    // Display the tasks
    document.getElementById("task-list").innerHTML = out;
    return;
  }

  // Get priority order from settings, or use default order if not set
  const priorityOrder = setdat.task_priority_order || [];

  // Helper function to check if a task is enabled and get its display info
  function getTaskDisplayInfo(taskId) {
    if (taskId.startsWith("gather_")) {
      const fieldName = taskId.replace("gather_", "").replace("_", " ");
      // Check if this field is enabled
      for (let i = 0; i < setdat.fields_enabled.length; i++) {
        if (setdat.fields_enabled[i] && setdat.fields[i] === fieldName) {
          const emoji = fieldEmojis[fieldName.replaceAll(" ", "_")] || "";
          return {
            enabled: true,
            title: `Gather ${i + 1}`,
            desc: `${emoji} ${fieldName}`,
          };
        }
      }
      return { enabled: false };
    }

    if (taskId.startsWith("collect_")) {
      const collectName = taskId.replace("collect_", "");

      // Handle special cases
      if (collectName === "sticker_printer") {
        if (!setdat.sticker_printer) return { enabled: false };
        return {
          enabled: true,
          title: "Collect",
          desc: `${collectEmojis.sticker_printer || ""} ${toTitleCase(
            "sticker printer"
          )}`,
        };
      }

      if (collectName === "sticker_stack") {
        if (!setdat.sticker_stack) return { enabled: false };
        return {
          enabled: true,
          title: "Collect Buff",
          desc: toImgArray(stickerStackIcon).join("<br>"),
        };
      }

      // Regular collect items
      if (!setdat[collectName]) return { enabled: false };
      const emoji = collectEmojis[collectName] || "";
      return {
        enabled: true,
        title: "Collect",
        desc: `${emoji} ${toTitleCase(collectName.replaceAll("_", " "))}`,
      };
    }

    if (taskId.startsWith("kill_")) {
      const mob = taskId.replace("kill_", "");
      // Check if this mob is enabled
      if (!setdat[mob]) return { enabled: false };
      const displayName = mob === "rhinobeetle" ? "rhino beetle" : mob;
      const emoji = killEmojis[mob] || "";
      return {
        enabled: true,
        title: "Kill",
        desc: `${emoji} ${toTitleCase(displayName.replaceAll("_", " "))}`,
      };
    }

    if (taskId.startsWith("quest_")) {
      const questName = taskId.replace("quest_", "");
      const questKey = `${questName}_quest`;
      if (!setdat[questKey]) return { enabled: false };
      const emoji = questGiverEmojis[questKey] || "";
      return {
        enabled: true,
        title: "Quest",
        desc: `${emoji} ${toTitleCase(questName.replaceAll("_", " "))}`,
      };
    }

    // Special tasks
    if (taskId === "blender") {
      if (!setdat.blender_enable) return { enabled: false };
      const selectedBlenderItems = {};
      for (let i = 1; i < 4; i++) {
        const item = setdat[`blender_item_${i}`]?.replaceAll(" ", "_");
        if (item == "none" || !item) continue;
        selectedBlenderItems[toTitleCase(item.replaceAll("_", " "))] =
          blenderIcons[item];
      }
      return {
        enabled: true,
        title: "Blender",
        desc: toImgArray(selectedBlenderItems).join("<br>"),
      };
    }

    if (taskId === "planters") {
      if (!setdat.planters_mode) return { enabled: false };
      const type = setdat.planters_mode == 1 ? "Manual" : "Auto";
      return {
        enabled: true,
        title: "Planters",
        desc: type,
      };
    }

    if (taskId === "mondo_buff") {
      if (!setdat.mondo_buff) return { enabled: false };
      return {
        enabled: true,
        title: "Collect",
        desc: `${collectEmojis.mondo_buff || ""} ${toTitleCase("mondo buff")}`,
      };
    }

    if (taskId === "stinger_hunt") {
      if (!setdat.stinger_hunt) return { enabled: false };
      return {
        enabled: true,
        title: "Kill",
        desc: `${killEmojis.stinger_hunt || ""} ${toTitleCase("stinger hunt")}`,
      };
    }

    if (taskId === "auto_field_boost") {
      if (!setdat.Auto_Field_Boost) return { enabled: false };
      return {
        enabled: true,
        title: "Collect Buff",
        desc: `${collectEmojis.Auto_Field_Boost || ""} ${toTitleCase(
          "auto field boost"
        )}`,
      };
    }

    if (taskId === "ant_challenge") {
      if (!setdat.ant_challenge) return { enabled: false };
      return {
        enabled: true,
        title: "Kill",
        desc: `${killEmojis.ant_challenge || ""} ${toTitleCase(
          "ant challenge"
        )}`,
      };
    }

    // Field boosters (blue_booster, red_booster, mountain_booster)
    if (
      taskId === "collect_blue_booster" ||
      taskId === "collect_red_booster" ||
      taskId === "collect_mountain_booster"
    ) {
      const boosterName = taskId.replace("collect_", "");
      if (!setdat[boosterName]) return { enabled: false };
      const emoji = fieldBoosterEmojis[boosterName] || "";
      return {
        enabled: true,
        title: "Collect Buff",
        desc: `${emoji} ${toTitleCase(boosterName.replaceAll("_", " "))}`,
      };
    }

    return { enabled: false };
  }

  // Show all tasks in priority order, but expand gather tasks to show all instances from fields array
  if (priorityOrder && priorityOrder.length > 0) {
    // Process each task in priority order
    for (const taskId of priorityOrder) {
      if (taskId.startsWith("gather_")) {
        // For gather tasks, show all instances of that field type from fields array
        const fieldName = taskId.replace("gather_", "").replace("_", " ");
        for (let i = 0; i < setdat.fields.length; i++) {
          if (setdat.fields_enabled[i] && setdat.fields[i] === fieldName) {
            const field = setdat.fields[i];
            out += taskHTML(
              `Gather ${i + 1}`,
              `${fieldEmojis[field.replaceAll(" ", "_")]} ${field}`
            );
          }
        }
      } else {
        // For non-gather tasks, show them normally
        const taskInfo = getTaskDisplayInfo(taskId);
        if (taskInfo.enabled) {
          out += taskHTML(taskInfo.title, taskInfo.desc);
        }
      }
    }
  } else {
    // Fallback to old order for non-gather tasks if no priority order is set
    //load quest givers
    for (const [k, v] of Object.entries(questGiverEmojis)) {
      if (!setdat[k]) continue;
      out += taskHTML(
        "Quest",
        `${v} ${toTitleCase(k.replaceAll("quest", "").replaceAll("_", " "))}`
      );
    }

    //load collect
    for (const [k, v] of Object.entries(collectEmojis)) {
      if (!setdat[k]) continue;
      out += taskHTML("Collect", `${v} ${toTitleCase(k.replaceAll("_", " "))}`);
    }
    //blender
    if (setdat["blender_enable"]) {
      const selectedBlenderItems = {};
      for (let i = 1; i < 4; i++) {
        const item = setdat[`blender_item_${i}`].replaceAll(" ", "_");
        if (item == "none") continue;
        selectedBlenderItems[toTitleCase(item.replaceAll("_", " "))] =
          blenderIcons[item];
      }
      out += taskHTML("Blender", toImgArray(selectedBlenderItems).join("<br>"));
    }
    //planters
    if (setdat["planters_mode"]) {
      const type = setdat["planters_mode"] == 1 ? "Manual" : "Auto";
      out += taskHTML("Planters", type);
    }
    //load kill
    for (let [k, v] of Object.entries(killEmojis)) {
      if (!setdat[k]) continue;
      if (k == "rhinobeetle") k = "rhino beetle";
      out += taskHTML("Kill", `${v} ${toTitleCase(k.replaceAll("_", " "))}`);
    }
    //load field boosters
    for (const [k, v] of Object.entries(fieldBoosterEmojis)) {
      if (!setdat[k]) continue;
      out += taskHTML(
        "Collect Buff",
        `${v} ${toTitleCase(k.replaceAll("_", " "))}`
      );
    }
    //load sticker stack
    for (const [k, v] of Object.entries(stickerStackIcon)) {
      if (!setdat[k]) continue;
      out += taskHTML(
        "Collect Buff",
        toImgArray(stickerStackIcon).join("<br>")
      );
    }
    
    //load gather tasks (enabled fields)
    for (let i = 0; i < setdat.fields_enabled.length; i++) {
      if (setdat.fields_enabled[i]) {
        const field = setdat.fields[i];
        const emoji = fieldEmojis[field.replaceAll(" ", "_")] || "";
        out += taskHTML(`Gather ${i + 1}`, `${emoji} ${field}`);
      }
    }
  }

  //display the tasks
  document.getElementById("task-list").innerHTML = out;

  //planter timers

  function getPlanterHTML(planter, field, harvestTime) {
    const currTime = Date.now() / 1000;
    const timeRemaining = secondsToMinsAndHours(harvestTime - currTime);
    return `
            <div class="planter">
                <img class="planter-img" src="./assets/icons/${planter.replaceAll(
                  " ",
                  "_"
                )}_planter.png">
                <div class="field-row">
                    <span>${toTitleCase(field)}</span>
                </div>
                <span class="time ${
                  timeRemaining == "Ready!" ? "ready" : ""
                }">${timeRemaining}</span> 
            </div> 
        `;
  }

  const planterTimerContainer = document.getElementById(
    "planter-timers-container"
  );
  if (setdat["planters_mode"]) {
    planterTimerContainer.classList.add("show");
    let planterData;
    const planterContainer =
      planterTimerContainer.querySelector(".planter-timers");
    let planterTimersOut = "";

    if (setdat["planters_mode"] == 1) {
      planterData = await eel.getManualPlanterData()();
      for (let i = 0; i < planterData.planters.length; i++) {
        if (planterData.planters[i]) {
          planterTimersOut += getPlanterHTML(
            planterData.planters[i],
            planterData.fields[i],
            planterData.harvestTimes[i]
          );
        }
      }
    } else if (setdat["planters_mode"] == 2) {
      planterData = (await eel.getAutoPlanterData()()).planters;
      for (const planter of planterData) {
        if (planter.planter) {
          planterTimersOut += getPlanterHTML(
            planter.planter,
            planter.field,
            planter.harvest_time
          );
        }
      }
    }
    planterContainer.innerHTML = planterTimersOut;
  } else {
    planterTimerContainer.classList.remove("show");
  }
}

eel.expose(closeWindow);
function closeWindow() {
  let new_window = open(location, "_self");
  new_window.top.close();
}

// Function to periodically check and update button state
async function checkAndUpdateButtonState() {
  try {
    const runState = await eel.getRunState()();
    // 2 = running, 3 = stopped, 6 = paused

    const settings = await loadAllSettings();
    const startKey = settings.start_keybind || "F1";
    const stopKey = settings.stop_keybind || "F3";
    // const pauseKey = settings.pause_keybind || "F2";

    const startBtn = document.getElementById("start-btn");
    const stopBtn = document.getElementById("stop-btn");
    // const pauseBtn = document.getElementById("pause-btn");

    if (runState === 2) {
      // Running: show Stop button
      if (startBtn) startBtn.style.display = "none";
      if (stopBtn) {
        stopBtn.style.display = "block";
        stopBtn.textContent = `Stop [${stopKey}]`;
      }
    } else {
      // Stopped or Paused: show Start button only
      if (startBtn) {
        startBtn.style.display = "block";
        startBtn.classList.remove("active");
        startBtn.disabled = false;
        startBtn.textContent = `Start [${startKey}]`;
      }
      if (stopBtn) stopBtn.style.display = "none";
    }

    // Update field-only mode dropdown to match current settings
    const macroModeDropdown = document.getElementById("macro_mode");
    if (macroModeDropdown && !isUserChangingMode) {
      const currentValue = settings.macro_mode || "normal";
      if (macroModeDropdown.value !== currentValue) {
        macroModeDropdown.value = currentValue;
      }
    }
  } catch (error) {
    console.error("Error checking button state:", error);
  }
}

// Start polling for button state updates
let buttonStateInterval;

$("#home-placeholder")
  .load("../htmlImports/tabs/home.html", async () => {
    await loadTasks();
    await updateStartButtonText();

    // Initialize macro mode dropdown
    const settings = await loadAllSettings();
    const macroModeDropdown = document.getElementById("macro_mode");
    if (macroModeDropdown && !isUserChangingMode) {
      const currentValue = settings.macro_mode || "normal";
      macroModeDropdown.value = currentValue;
    }

    // Start checking button state every 500ms
    buttonStateInterval = setInterval(checkAndUpdateButtonState, 500);
  }) //load home tab
  .on("unload", () => {
    // Stop polling when tab is unloaded
    if (buttonStateInterval) {
      clearInterval(buttonStateInterval);
      buttonStateInterval = null;
    }
  })
  .on("click", "#log-btn", (event) => {
    //log button
    const result = purpleButtonToggle(event.currentTarget, [
      "Simple",
      "Detailed",
    ]);
    document.getElementById("log-type").innerText = result;
  })
  .on("click", "#start-btn", async (event) => {
    //start button - only used when macro is stopped
    eel.start();
    // Update button state optimistically (show stop button immediately)
    const settings = await loadAllSettings();
    const stopKey = settings.stop_keybind || "F3";
    const startBtn = document.getElementById("start-btn");
    const stopBtn = document.getElementById("stop-btn");
    if (startBtn) startBtn.style.display = "none";
    if (stopBtn) {
      stopBtn.style.display = "block";
      stopBtn.textContent = `Stop [${stopKey}]`;
    }
  })
  .on("click", "#stop-btn", async (event) => {
    //stop button - stops the macro completely
    eel.stop();
    // Update button state optimistically (show start button immediately)
    const settings = await loadAllSettings();
    const startKey = settings.start_keybind || "F1";
    const startBtn = document.getElementById("start-btn");
    const stopBtn = document.getElementById("stop-btn");
    if (startBtn) {
      startBtn.style.display = "block";
      startBtn.classList.remove("active");
      startBtn.disabled = false;
      startBtn.textContent = `Start [${startKey}]`;
    }
    if (stopBtn) stopBtn.style.display = "none";
  })
  // .on("click", "#pause-btn", async (event) => {
  //   //pause/resume button - toggle between pause and resume
  //   const runState = await eel.getRunState()();
  //   if (runState === 2) {
  //     // Running -> Pause
  //     eel.pause();
  //   } else if (runState === 6) {
  //     // Paused -> Resume
  //     eel.resume();
  //   }
  // })
  .on("click", "#update-btn", async (event) => {
    //start button
    if (!event.currentTarget.classList.contains("active")) {
      purpleButtonToggle(event.currentTarget, ["Update", "Updating"]);
      await eel.update();
    }
  })
  .on("click", "#clear-timers-btn", async (event) => {
    const btn = event.currentTarget;
    if (btn.classList.contains("active")) return;
    btn.classList.add("active");
    const setdat = await loadAllSettings();
    if (setdat["planters_mode"] == 1) {
      eel.clearManualPlanters();
    } else if (setdat["planters_mode"] == 2) {
      eel.clearAutoPlanters();
    }
    document
      .getElementById("planter-timers-container")
      .querySelector(".planter-timers").innerHTML = "";
    setTimeout(() => {
      btn.classList.remove("active");
    }, 700);
  })
  .on("change", "#macro_mode", async (event) => {
    // Set flag to prevent updates during user interaction
    isUserChangingMode = true;

    try {
      // Handle macro mode dropdown
      const selectedValue = event.currentTarget.value;

      await eel.saveGeneralSetting("macro_mode", selectedValue);

      // Small delay before reloading tasks to ensure backend is updated
      await new Promise((resolve) => setTimeout(resolve, 10));

      // Reload tasks to reflect the change
      await loadTasks();
    } finally {
      // Clear the flag after a short delay to allow any pending updates
      setTimeout(() => {
        isUserChangingMode = false;
      }, 100);
    }
  });
