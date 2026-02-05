//use javascript to add html elements
//avoids repetition of building the same elements

//commonly used
const slotArray = [1, 2, 3, 4, 5, 6, 7];

//id: id of input element
/*
    type property: the type of input element
    checkbox:
    type: {
        name: "checkbox",
        triggerFunction: "saveData()"
    }
    dropdown:
    type: {
        name: "dropdown",
        data: ["a","b","c"],
        triggerFunction: "saveData()",
        length: 13 //in rem units, defaults to 10 if not included
    }
    textbox:
    type: {
        name: "textbox",
        length: 13, //in rem units, defaults to 10 if not included
        triggerFunction: "saveData()",
        inputType: "float", //restrict the input values to only certain characters. Options are: string, float, int
        inputLimit: 5 //restrict the maximum number of characters allowed. If set to 0 or not included, no limit 
    }
    button:
    type: {
        name: "button",
        triggerFunction: "func()",
        text: "reset" //button text
        length: 10, //in rem units, defaults to 5 if not included
    }
*/

//create option elements in a already existing dropdown
//id: id of dropdown element
//data: array of values to set
function setDropdownData(id, data) {
  //create the html
  html = "";
  data.forEach((x) => {
    html += `<div class = "option" data-value = "${x}">${x}</div>`;
  });
  //add it to the element
  document.getElementById(id).children[1].children[0].innerHTML = html;
}

function buildInput(id, type) {
  if (type.name == "checkbox") {
    return `<label class="checkbox-container" style="margin-top: 0.6rem;">
                    <input type="checkbox" id = ${id} onchange="${type.triggerFunction}">
                    <span class="checkmark"></span>
                </label>`;
  } else if (type.name == "dropdown") {
    let html = `
        <div data-onchange="${
          type.triggerFunction
        }" id = ${id} class="custom-select poppins-regular" style="width: ${
      type.length ? type.length : 10
    }rem; margin-top: 0.6rem;">
            <div class="select-area">
                <div class = "value" data-value="none">None</div>
                <div class = "chevron">></div>
            </div>
            <div class="select-menu-relative">
                <div class="select-menu" style="display: none;">
        `;
    for (let i = 0; i < type.data.length; i++) {
      const x = type.data[i];
      let value = x;
      if ($.type(value) === "string") {
        value = stripHTMLTags(value);
        value = value.replace(/[^\p{L}\p{N}\p{P}\p{Z}^$\n]/gu, ""); //remove emojis
        value = value.trim().toLowerCase(); //remove leading/trailing white space, also set to lowercase
      }
      html += `<div class = "option" data-value = "${value}">${x}</div>`;
    }
    html += `</div>
            </div>
        </div>`;
    return html;
  } else if (type.name == "textbox") {
    let html = `<input type="text" id="${id}" style="width: ${
      type.length ? type.length : 10
    }rem; margin-top: 0.6rem;" class="poppins-regular textbox" data-input-type="${
      type.inputType
    }" data-input-limit="${
      type.inputLimit ? type.inputLimit : 0
    }" onkeypress="return textboxRestriction(this, event)" onchange="${
      type.triggerFunction
    }">`;
    return html;
  } else if (type.name == "button") {
    let html = `<div id = "${id}" class="purple-button" onclick="${
      type.triggerFunction
    }" style="width: ${
      type.length ? type.length : 5
    }rem; display: flex; justify-content: center; padding: 0.3rem; cursor: pointer;">${
      type.text
    }</div>`;
    return html;
  } else if (type.name == "keybind") {
    let html = `<div id="${id}" class="keybind-input poppins-regular" style="width: ${
      type.length ? type.length : 10
    }rem; margin-top: 0.6rem; padding: 0.5rem; border: 2px solid #7A77BB; border-radius: 4px; background: #2F3136; color: #d2d3d2; cursor: pointer; text-align: center; user-select: none; font-size: 1rem; transition: all 0.2s ease;" onclick="startKeybindRecording('${id}')" data-recording="false" data-trigger-function="${
      type.triggerFunction
    }">
            <span class="keybind-display">Click to record</span>
        </div>`;
    return html;
  } else if (type.name == "draglist") {
    let html = `<div id="${id}" class="drag-list" data-onchange="${type.triggerFunction}" style="margin-top: 0.6rem;">
            <div class="drag-list-container" id="${id}-container">`;
    for (let i = 0; i < type.data.length; i++) {
      const item = type.data[i];
      html += `<div class="drag-item" data-id="${item.id}" draggable="true">
                <span class="drag-handle">⋮⋮</span>
                <span class="drag-text">${item.name}</span>
            </div>`;
    }
    html += `</div></div>`;
    return html;
  }
}

//parentElement: the parentElement to add the container to
//build a standard container for settings
//title: title of container
//settings: an array of objects
/*
[
    {
        id: "field-enable",
        title: "enable task",
        desc: "Enable gathering in field",
        type: input-type-object-here
    }
]
*/
function buildStandardContainer(parentElement, title, desc, settings) {
  let out = `
        <div class = "poppins-medium standard-container" style="display: block; justify-items: unset; padding-top: 1rem;">
            <h2 id="${title.toLowerCase().replaceAll(" ", "-")}">${title}</h2>
            <p style = "font-weight:500; font-size:1rem;">${desc}</p>
            <div class="seperator"></div>
    `;
  //adjust padding right on the form based on the input type
  const inputPadding = {
    checkbox: "10%",
    dropdown: "5%",
    textbox: "5%",
    button: "5%",
    keybind: "5%",
  };

  //add each setting
  settings.forEach((e, i) => {
    //note: if i > 0, set a margin-top
    //is it better to setup a parent div and use gap instead? yes
    out += `
        <form style="display: flex; align-items:flex-start; justify-content: space-between; padding-right: ${
          inputPadding[e.type.name]
        }; ${i ? "margin-top:1rem" : ""}";>
            <div style="width: 70%;">
                <label>${e.title}</label>
                <p>${e.desc}</p>
            </div>
            ${buildInput(e.id, e.type)}
        </form>
        `;
    out += "</form>";
  });

  out += "</div>";
  parentElement.innerHTML += out;
}
