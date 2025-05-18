

function switchKillTab(target){
    //hide all tabs

    //remove the arrow indicator
    const selector = document.getElementById("kill-select")
    if (selector) selector.remove()
    //remove active class and hide all tabs
    Array.from(document.getElementsByClassName("kill-tab-item")).forEach(x => {
        x.classList.remove("active")
        document.getElementById(`${x.id}-tab`).style.display = "none"
    })
    //add indicator + active class
    target.classList.add("active")
    target.innerHTML = `<div class = "select-indicator" id = "kill-select"></div>` + target.innerHTML
    //show tab
    tab = document.getElementById(`${target.id}-tab`)
    tab.style.display = "block"
    //scroll back to top
    tab.scrollTo(0,0); 
}

function loadKill(){
    switchKillTab(document.getElementById("kill-settings"))
}

$("#kill-placeholder")
.load("../htmlImports/tabs/kill.html", loadKill) //load kill tab
.on("click", ".kill-tab-item", (event) => switchKillTab(event.currentTarget)) //navigate between tabs