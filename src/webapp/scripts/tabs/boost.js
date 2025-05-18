

function switchBoostTab(target){
    //hide all tabs

    //remove the arrow indicator
    const selector = document.getElementById("boost-select")
    if (selector) selector.remove()
    //remove active class and hide all tabs
    Array.from(document.getElementsByClassName("boost-tab-item")).forEach(x => {
        x.classList.remove("active")
        document.getElementById(`${x.id}-tab`).style.display = "none"
    })
    //add indicator + active class
    target.classList.add("active")
    target.innerHTML = `<div class = "select-indicator" id = "boost-select"></div>` + target.innerHTML
    //show tab
    tab = document.getElementById(`${target.id}-tab`)
    tab.style.display = "block"
    //scroll back to top
    tab.scrollTo(0,0); 
}

function loadBoost(){
    switchBoostTab(document.getElementById("boost-hotbar"))
}


function clearAFBData(ele){
    if (ele.classList.contains("active")) return
    eel.clearAFB()
    ele.classList.add("active")
    setTimeout(() => {
        ele.classList.remove("active")
      }, 700)
}

$("#boost-placeholder")
.load("../htmlImports/tabs/boost.html", loadBoost) //load kill tab
.on("click", ".boost-tab-item", (event) => switchBoostTab(event.currentTarget)) //navigate between tabs