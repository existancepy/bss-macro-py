/*
=============================================
Planters Tab
=============================================
*/

//when the planter slider changes
function changePlanterMode(){
    const ele = document.getElementById("planters_mode")
    saveSetting(ele, 'profile')
    //show the corresponding tab
    const planterMode = {
        1: "manual",
        2: "auto"
    }
    Array.from(document.getElementsByClassName("planter-tab")).forEach(x => x.style.display="none")
    //ele.value doesnt
    if (ele.value > 0) document.getElementById(`planters-${planterMode[ele.value]}`).style.display = "block"
    
}

const planterArray = toImgArray(planterIcons)
const fieldNectarArray = toImgArray(fieldNectarIcons, true)

function fieldDropDownHTML(id){
    return buildInput(id,{
        name: "dropdown",
        data: fieldNectarArray,
        triggerFunction: "saveSetting(this, 'profile')",
        length: 11.5    
    })
}
function planterDropDownHTML(id){
    return buildInput(id,{
        name: "dropdown",
        data: planterArray,
        triggerFunction: "saveSetting(this, 'profile')",
        length: 11.5
    })
}

async function loadPlanters(){
    const cycleElement = document.getElementById("manual-planters-cycles")
    for (i=1; i < 6;i++){
        const html = 
        `
        <div class="seperator" style="margin-bottom: 1rem;"></div>
        <h3 class="poppins-semibold">Cycle ${i}</h3>
        <table style="margin-top: 1rem; row-gap: 1rem;">
            <tr>
                <td><h4 class="poppins-regular">Planters:</h4></td>
                <td>${planterDropDownHTML(`cycle${i}_1_planter`)}</td>
                <td>${planterDropDownHTML(`cycle${i}_2_planter`)}</td>
                <td>${planterDropDownHTML(`cycle${i}_3_planter`)}</td>
            </tr>
            <tr>
                <td><h4 class="poppins-regular">Fields:</h4></td>
                <td>${fieldDropDownHTML(`cycle${i}_1_field`)}</td>
                <td>${fieldDropDownHTML(`cycle${i}_2_field`)}</td>
                <td>${fieldDropDownHTML(`cycle${i}_3_field`)}</td>
            </tr>
            <tr>
                <td>
                    <h4 class="poppins-regular">Gather in Planter Field:</h4>
                    <div class="poppins-regular" style="font-size:0.9rem; color: #adb4bc">The field's gather settings match<br>those in the gather tab</div>
                </td>
                
                <td><label class="checkbox-container" style="margin-top:-0.6rem">
                    <input type="checkbox" id = "cycle${i}_1_gather" onchange="saveSetting(this, 'profile')">
                    <span class="checkmark"></span>
                </label></td>
                <td><label class="checkbox-container" style="margin-top:-0.6rem">
                    <input type="checkbox" id = "cycle${i}_2_gather" onchange="saveSetting(this, 'profile')">
                    <span class="checkmark"></span>
                </label></td>
                <td><label class="checkbox-container" style="margin-top:-0.6rem">
                    <input type="checkbox" id = "cycle${i}_3_gather" onchange="saveSetting(this, 'profile')">
                    <span class="checkmark"></span>
                </label></td>
            </tr>
            <tr>
                <td>
                    <h4 class="poppins-regular">Glitter:</h4>
                    <div class="poppins-regular" style="font-size:0.9rem; color: #adb4bc">Use Glitter when the placing a planter.<br>Speeds up planter growth by 25%</div>
                </td>
                <td><label class="checkbox-container" style="margin-top:-1.2rem">
                    <input type="checkbox" id = "cycle${i}_1_glitter" onchange="saveSetting(this, 'profile')">
                    <span class="checkmark"></span>
                </label></td>
                <td><label class="checkbox-container" style="margin-top:-1.2rem">
                    <input type="checkbox" id = "cycle${i}_2_glitter" onchange="saveSetting(this, 'profile')">
                    <span class="checkmark"></span>
                </label></td>
                <td><label class="checkbox-container" style="margin-top:-1.2rem">
                    <input type="checkbox" id = "cycle${i}_3_glitter" onchange="saveSetting(this, 'profile')">
                    <span class="checkmark"></span>
                </label></td>
            </tr>
        </table>
        `
        cycleElement.innerHTML += html
    }
    //load inputs
    const settings = await loadAllSettings()
    loadInputs(settings)
    //show the planter tab
    changePlanterMode()
}

function clearManualPlantersData(){
    const btn = document.getElementById("manual-planters-reset-btn")
    if (btn.classList.contains("active")) return
    eel.clearManualPlanters()
    btn.classList.add("active")
    setTimeout(() => {
        btn.classList.remove("active")
      }, 700)
}
$("#planters-placeholder")
.load("../htmlImports/tabs/planters.html", loadPlanters) 
