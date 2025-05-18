/*
=============================================
Config Tab
=============================================
*/

async function switchConfigTab(target){
    //remove the active classes and hide all tabs
    Array.from(document.getElementsByClassName("settings-tab-item")).forEach(x => {
        x.classList.remove("active")
        document.getElementById(x.id.split("-")[1]).style.display = "none"
    }) 
    //add active class
    target.classList.add("active")
    //get the element of the page to show
    const showElement = document.getElementById(target.id.split("-")[1])
    showElement.style.display = "block"
    //scroll back to top
    showElement.scrollTo(0,0); 
}


async function loadConfig(){
    const settings = await loadAllSettings()
    loadInputs(settings)
    switchConfigTab(document.getElementById("setting-bss"))
}

$("#config-placeholder", loadConfig)
.load("../htmlImports/tabs/config.html") //load config tab
.on("click", ".settings-tab-item", (event) => switchConfigTab(event.currentTarget)) //navigate between fields
