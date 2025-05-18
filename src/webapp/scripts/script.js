
//change the styling of the purple buttons
//element: the purple button element
//label: the text labels of the button [not-active-label, active-label]
function purpleButtonToggle(element, labels){
    //check for active class
    if (element.classList.contains("active")){
        element.innerText = labels[0]
        element.classList.remove("active")
        return labels[1]
    }

    element.innerText = labels[1]
    element.classList.add("active")
    return labels[0]
    
}

//get the value of input elements like checkboxes, dropdown and textboxes
function getInputValue(id){
    const ele = document.getElementById(id)
    //checkbox
    if (ele.tagName == "INPUT" && ele.type == "checkbox"){
        return ele.checked
    //textbox
    } else if (ele.tagName == "INPUT" && ele.type == "text"){
        const value = ele.value
        if (!value && (ele.dataset.inputType == "float" || ele.dataset.inputType == "int")) return 0
        if (!value) return ""
        return value
    //custom dropdown
    } else if (ele.tagName == "DIV" && ele.className.includes("custom-select")){
        return getDropdownValue(ele).toLowerCase()
    //slider
    } else if (ele.tagName == "INPUT" && ele.type == "range"){
        return ele.value
    }
}

async function loadSettings(){
    return await eel.loadSettings()()
}

async function loadAllSettings(){
    return await eel.loadAllSettings()()
}
//save the setting
//element
//type: setting type, eg: profile, general
function saveSetting(ele, type){
    const id = ele.id
    const value = getInputValue(id)
    if (type == "profile"){
        eel.saveProfileSetting(id, value)
    }else if (type == "general"){
        eel.saveGeneralSetting(id, value)
    }
}

//returns a object based on the settings
//proprties: an array of property names
//note: element corresponding to the property must have the same id as that property
function generateSettingObject(properties){
    let out = {}
    properties.forEach(x => {
        out[x] = getInputValue(x)
    })
    return out
}

//load fields based on the obj data
eel.expose(loadInputs)
function loadInputs(obj){
    for (const [k,v] of Object.entries(obj)) {
        const ele = document.getElementById(k)
        //check if element exists
        if (!ele) continue
        if (ele.type == "checkbox"){
            ele.checked = v
        }else if (ele.className.includes("custom-select")){
            setDropdownValue(ele, v)
        }else{
            ele.value = v
        }
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
    var charCode = (evt.which) ? evt.which : evt.keyCode
    if (ele.dataset.inputLimit != 0 && ele.value.length >= ele.dataset.inputLimit) return false
    if (ele.dataset.inputType == "float"){
        if (charCode == 46) {
            //Check if the text already contains the . character
            if (ele.value.indexOf('.') === -1) {
                return true
            } else {
                return false
            }
        } else {
            if (charCode > 31 && (charCode < 48 || charCode > 57)) return false
        }
        return true;
    } else if (ele.dataset.inputType == "int"){
        return !(charCode > 31 && (charCode < 48 || charCode > 57))
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
window.addEventListener("keydown", (event) => {
    const key = event.key
    const disabledKeys = ["F1","F3","F5","F12"]
    if (disabledKeys.includes(key)){
        event.preventDefault()
        event.stopPropagation()
        return false
    } else if (event.ctrlKey && event.shiftKey && event.key == "I") {
        // block Strg+Shift+I (DevTools)
        event.preventDefault()
        event.stopPropagation()
        return false
    } else if (event.ctrlKey && event.shiftKey && event.key == "J") {
    // block Strg+Shift+J (Console)
    event.preventDefault()
    event.stopPropagation()
    return false
}
})

/*
=============================================
Custom Select
=============================================
*/
dropdownOpen = false
//pass an optionEle to set the select-area
function updateDropDownDisplay(optionEle){
    const parentEle = optionEle.parentElement.parentElement.parentElement
    //set the data-value attribute of the select
    const selectEle = parentEle.children[0].children[0]
    selectEle.dataset.value = optionEle.dataset.value
    //set the display to match the option
    selectEle.innerHTML = optionEle.innerHTML
}
//document click event
function dropdownClicked(event){
    //get the element that was clicked
    const ele = event.target
    if (!ele){
        dropdownOpen = false
        return
    } 
    //toggle dropdown
    if (ele.className.includes("select-area")){
        //get the associated custom-select parent element
        const parent = ele.parentElement
        const optionsEle = parent.children[1].children[0]
        closeAllDropdowns(optionsEle) //close all other dropdowns
        //toggle the dropdown menu
        if (dropdownOpen !== optionsEle){ //open it
            dropdownOpen = optionsEle
            optionsEle.style.display = "block"
            const currValue = parent.children[0].children[0].dataset.value
            //highlight the corresponding value option
            //ie if the value of the dropdown is "none", highlight the "none option"
            Array.from(optionsEle.children).forEach(x => {
                x.dataset.value == currValue ? x.classList.add("selected") : x.classList.remove("selected")
            })
            //check if its going below the screen and render the menu above
            parent.style.transform = "none"
            optionsEle.style.transform = "none"
            ele.style.transform = "none"
            const height = optionsEle.getBoundingClientRect().height
            const y = optionsEle.getBoundingClientRect().top
            //check if it goes below the screen
            //if it is flipped and goes above the screen, prioritise rendering the dropdown down
            if (height + y > window.innerHeight && y > height){
                parent.style.transform = "rotate(180deg)" //render the dropdown menu above
                //flip everything to face the correct direction
                optionsEle.style.transform = "rotate(180deg)"
                ele.style.transform = "rotate(180deg)"
            }
        }
        else{ //close it
            optionsEle.style.display = "none"
            dropdownOpen = false
        }
    }
    else{
        //close all dropdowns, because an option was selected or the user clicked elsewhere
        closeAllDropdowns()
        if (ele.className.includes("option")){
            updateDropDownDisplay(ele)
            const parentEle = ele.parentElement.parentElement.parentElement
            let funcParams = parentEle.dataset.onchange.replace("this", "parentEle")
            eval(funcParams)
            dropdownOpen = false
        }
        else{
            //try again, but with the parent element
            //this creates a recursive loop to account for children elements (could be expensive)
            dropdownClicked({target: ele.parentElement})
        }
    }
}

function getDropdownValue(ele){
    return ele.children[0].children[0].dataset.value
}

function setDropdownValue(ele, value){
    const optionsEle = ele.children[1].children[0]
    for (let i = 0; i < optionsEle.children.length; i++){
        const x = optionsEle.children[i]
        if (x.dataset.value == value){
            updateDropDownDisplay(x)
            break
        }
    }
}
//close all other dropdown menus
//if ele is undefined, close all menus
function closeAllDropdowns(ele){
    Array.from(document.getElementsByClassName("select-menu")).forEach(x => {
        if (ele !== x) x.style.display="none"
    })
}
function dropdownHover(event){
    const ele = event.target
    if (ele.className.includes("option")){
        Array.from(document.getElementsByClassName("option")).forEach(x => {
            x.classList.remove("selected")
        })
        ele.classList.add("selected")
    }
}
document.addEventListener("click", dropdownClicked);
document.addEventListener("mouseover", dropdownHover);