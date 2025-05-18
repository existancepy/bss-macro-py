/*
=============================================
Tab bar
=============================================
*/

//switch tab
//start by hiding all tabs, then show the one that is relevant
//also remove all tabs' active class and add it back to the target one
function switchTab(event){
    const tabName = event.currentTarget.id.split("-")[0]
    //remove and hide
    Array.from(document.getElementsByClassName("content")).forEach(x => {
        x.style.display = "none"
    })
    Array.from(document.getElementsByClassName("sidebar-item")).forEach(x => {
        x.classList.remove("active")
    })
    //add and show
    event.currentTarget.classList.add("active")
    document.getElementById(`${tabName}-placeholder`).style.display = "flex"
}
//load and add event handlers
$("#tabs-placeholder")
.load("../htmlImports/persistent/tabs.html")
.on("click",".sidebar-item", switchTab)