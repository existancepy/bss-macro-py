/*
=============================================
Collect Tab
=============================================
*/


function clearBlenderData(ele){
    if (ele.classList.contains("active")) return
    eel.clearBlender()
    ele.classList.add("active")
    setTimeout(() => {
        ele.classList.remove("active")
      }, 700)
}

async function loadCollect(){
    const settings = await loadAllSettings()
    loadInputs(settings)
}

$("#collect-placeholder", loadCollect)
.load("../htmlImports/tabs/collect.html") //load config tab
