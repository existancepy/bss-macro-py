/*
=============================================
Home Tab
=============================================
*/

//use a python function to open the link in the user's actual browser
function ahref(link){
    eel.openLink(link)
}

//toggle the start/stop button visuals
eel.expose(toggleStartStop)
function toggleStartStop(){
    return purpleButtonToggle(document.getElementById("start-btn"), ["Start [F1]","Stop [F3]"])
}

eel.expose(log)
function log(time = "", msg = "", color = ""){
    document.getElementById("log")
    let timeText = ""
    if (time) timeText = `[${time}]`
    const html = `
    <div class = "log-msg"><span style="background-color: #${color}; align-self: start"></span>${timeText} ${msg}</div>
    `
    const logs = document.getElementById("logs")
    logs.innerHTML += html
    logs.scrollTop = logs.scrollHeight;
}

//returns a html string for the task
function taskHTML(title, desc=""){
    const html = `
    <div style="margin-top: 1rem;">
        <div style="font-size: 1.1rem;">${title}</div>
        <div style="font-size: 0.9rem; color: #ADB5BD; display:flex; align-items:center;">${desc.includes('<img') ? desc : toTitleCase(desc)}</div>
        <div style="background-color: #949393; height: 1px; width: 95%; margin-top: 0.4rem;"></div>
    </div>
    `
    return html
}

function secondsToMinsAndHours(time){
    if (time < 0) return "Ready!"
    const hours = Math.floor(time / 3600)
    const minutes = Math.floor((time - hours*3600)/60)
    return `${hours}h ${minutes}m`
}

//load the tasks
//also set max-height for logs
eel.expose(loadTasks)
async function loadTasks(){
    const setdat = await loadAllSettings()
    let out = ""
    //load quest givers
    for (const [k, v] of Object.entries(questGiverEmojis)) {
        if (!setdat[k]) continue
        out += taskHTML("Quest", `${v} ${toTitleCase(k.replaceAll("quest","").replaceAll("_", " "))}`)
    }
    
    //load collect
    for (const [k, v] of Object.entries(collectEmojis)) {
        if (!setdat[k]) continue
        out += taskHTML("Collect", `${v} ${toTitleCase(k.replaceAll("_", " "))}`)
    }
    //blender
    if (setdat["blender_enable"]){
        const selectedBlenderItems = {}
        for (let i = 1; i < 4; i++){
            const item = setdat[`blender_item_${i}`].replaceAll(" ","_")
            if (item == "none") continue
            selectedBlenderItems[toTitleCase(item.replaceAll("_"," "))] = blenderIcons[item]
        }
        out += taskHTML("Blender", toImgArray(selectedBlenderItems).join("<br>"))
    }
    //planters
    if (setdat["planters_mode"]){
        const type = setdat["planters_mode"] == 1 ? "Manual" : "Auto"
        out += taskHTML("Planters", type)
    }
    //load kill
    for (let [k, v] of Object.entries(killEmojis)) {
        if (!setdat[k]) continue
        if (k == "rhinobeetle") k = "rhino beetle"
        out += taskHTML("Kill", `${v} ${toTitleCase(k.replaceAll("_", " "))}`)
    }
    //load field boosters
    for (const [k, v] of Object.entries(fieldBoosterEmojis)) {
        if (!setdat[k]) continue
        out += taskHTML("Collect Buff", `${v} ${toTitleCase(k.replaceAll("_", " "))}`)
    }
    //load sticker stack
    for (const [k, v] of Object.entries(stickerStackIcon)) {
        if (!setdat[k]) continue
        out += taskHTML("Collect Buff", toImgArray(stickerStackIcon).join("<br>"))
    }
    //load the gather
    for(let i = 0; i <= setdat.fields_enabled.length; i++){
        if (!setdat.fields_enabled[i]) continue
        const field = setdat.fields[i]
        out += taskHTML(`Gather ${i+1}`,`${fieldEmojis[field.replaceAll(" ","_")]} ${field}`)
    }
    //display the tasks
    document.getElementById("task-list").innerHTML = out

    //planter timers

    function getPlanterHTML(planter, field, harvestTime){
        const currTime = Date.now() / 1000
        const timeRemaining = secondsToMinsAndHours(harvestTime - currTime)
        return `
            <div class="planter">
                <img class="planter-img" src="./assets/icons/${planter.replaceAll(" ", "_")}_planter.png">
                <div class="field-row">
                    <span>${toTitleCase(field)}</span>
                    <img src="./assets/icons/${fieldNectarIcons[field.toLowerCase().replaceAll(" ","_")]}.png">
                </div>
                <span class="time ${timeRemaining == "Ready!" ? 'ready' : ''}">${timeRemaining}</span> 
            </div> 
        `
    }

    const planterTimerContainer = document.getElementById("planter-timers-container")
    if (setdat["planters_mode"]){
        planterTimerContainer.classList.add("show")
        let planterData
        const planterContainer = planterTimerContainer.querySelector(".planter-timers")
        let planterTimersOut = ""

        if (setdat["planters_mode"] == 1){
            planterData = await eel.getManualPlanterData()()
            for(let i = 0; i< planterData.planters.length; i++){
                if (planterData.planters[i]){
                    planterTimersOut += getPlanterHTML(planterData.planters[i], planterData.fields[i], planterData.harvestTimes[i])
                }
            }
        }else if(setdat["planters_mode"] == 2){
            planterData = (await eel.getAutoPlanterData()()).planters
            for (const planter of planterData) {
                if (planter.planter){
                    planterTimersOut += getPlanterHTML(planter.planter, planter.field, planter.harvest_time)
                }
            }
        }
        planterContainer.innerHTML = planterTimersOut
    }
    else{
        planterTimerContainer.classList.remove("show")
    }
}

eel.expose(closeWindow)
function closeWindow() {
    let new_window = open(location, '_self');
    new_window.top.close();
}


$("#home-placeholder")
.load("../htmlImports/tabs/home.html", loadTasks) //load home tab
.on("click", "#log-btn",(event) => { //log button
    const result = purpleButtonToggle(event.currentTarget, ["Simple","Detailed"])
    document.getElementById("log-type").innerText = result
})
.on("click", "#start-btn",(event) => { //start button
    //no need to change display, python will trigger toggleStartStop
    if (event.currentTarget.classList.contains("active")){
        eel.stop()
    }else{
        eel.start()
    }
})
.on("click", "#update-btn", async (event) => { //start button
    if (!event.currentTarget.classList.contains("active")){
        purpleButtonToggle(event.currentTarget, ["Update","Updating"])
        await eel.update()
    }
})
.on("click", "#clear-timers-btn", async(event) => {
    const btn = event.currentTarget
    if (btn.classList.contains("active")) return
    btn.classList.add("active")
    const setdat = await loadAllSettings()
    if (setdat["planters_mode"] == 1){
        eel.clearManualPlanters()
    }else if(setdat["planters_mode"] == 2){
        eel.clearAutoPlanters()
    }
    document.getElementById("planter-timers-container").querySelector(".planter-timers").innerHTML = ""
    setTimeout(() => {
        btn.classList.remove("active")
      }, 700)
})