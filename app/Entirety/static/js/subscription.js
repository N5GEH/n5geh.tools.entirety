htmx.on("htmx:afterSwap", (e) => {
    // Response targeting #dialog => show the modal
    if (e.detail.target.id == "div_entities") {
        updateRemoveListeners();
    }
})

function hideElement(id) {
    let element=document.getElementById(id);
    if (element) {
        // type element is not removed, so try
        // to work with that first
        if (element.hasAttribute("type")) {
            element.setAttribute("type", "hidden");
            element.value = "---";
        }
        else {
            element.setAttribute("hidden", "hidden");
            element.selectedIndex = -1;
        }
    }
    else {
        console.error("Failed to get element with id: ", id);
    }
}

function showElement(id) {
    let element=document.getElementById(id);
    if (element) {
        // type element is not removed, so try
        // to work with that first
        if (element.hasAttribute("type")) {
            element.setAttribute("type", "text");
            if (element.value == "---") {
                element.value = "";
            }
        }
        else if (element.hasAttribute("hidden")) {
            element.removeAttribute("hidden");
        }
        else console.error("Failed to show element with id: ", id);
    }
    else {
        console.error("Failed to get element with id: ", id);
    }
}

function workAroundInconsistentNamingConvention(name) {
    if (name == "type") {
        return "entity_type";
    }
    if (name == "entity") {
        return "entity_id";
    }
    console.error("don't recognise name: ", name);
    return "";
}

function updateEntityList(value, id) {
    parts  = id.split('-');
    prefix = "id_entity-" + parts[1];
    name = parts[2].slice(0, -9);
    element0 = prefix + "-" + workAroundInconsistentNamingConvention(name) + "_0";
    element1 = prefix + "-" + workAroundInconsistentNamingConvention(name) + "_1";
    if (value == "id" || value == "type") {
        showElement(element0);
        hideElement(element1);
    }
    else if (value == "id_pattern" || value == "type_pattern") {
        showElement(element1);
        hideElement(element0);
    }
    else {
        console.error("I don't know how to update entity list element: ",
                      elementId0, " with value: ", value, " and id: ", id);
    }
}

updateRemoveListeners();

function updateRemoveListeners() {
    let removeButton = document.querySelectorAll(".remove-entity");
    removeButton.forEach(function (elem) {
        elem.addEventListener("click", removeEntity, {once: true});
    });
}

function removeEntity(event) {
    event.preventDefault();

    let pivotForm = document.querySelector('.entity-form')

    let prefix = pivotForm.querySelector('fieldset').querySelector('div').getAttribute("id").split("-")[0].split("_").pop();
    let totalForms = document.getElementById('id_' + prefix + '-TOTAL_FORMS');
    let formCount = parseInt(totalForms.value);

    totalForms.value = formCount - 1;

    let elem = event.currentTarget;
    if (elem.parentElement.classList.contains("entity-form")) {
        elem.parentElement.remove();
    }

    let allForms = document.querySelectorAll('.entity-form')

    // seems to work, but quite hacky
    for (let i = 0; i < allForms.length; i++) {
        let elements = allForms[i].querySelectorAll("[id*='id_" + prefix + "']");
        elements.forEach(function (item, index) {
            let parts = item.id.split("-");
            parts[1] = i;
            item.id = parts.join("-");
            if(item.hasAttribute("name")){
                parts = item.getAttribute("name").split("-")
                parts[1] = i;
                item.setAttribute("name",parts.join("-"));
            }

        });
        elements = allForms[i].querySelectorAll("[for^='id_" + prefix + "']");
         elements.forEach(function (item, index) {
            let parts = item.getAttribute("for").split("-");
            parts[1] = i;
            item.setAttribute("for", parts.join("-"));
        });
    }
}

function showMqttSection() {
    var mqtt = document.getElementById('mqtt');
    var mqttCustom = document.getElementById('mqttCustom');
    var http = document.getElementById('http');
    var httpCustom = document.getElementById('httpCustom');

    // Show only MQTT section
    mqtt.classList.remove('d-none');
    mqtt.classList.add('d-block');

    // Hide HTTP and other sections
    http.classList.add('d-none');
    http.classList.remove('d-block');
    httpCustom.classList.add('d-none');
    httpCustom.classList.remove('d-block');
    mqttCustom.classList.add('d-none');
    mqttCustom.classList.remove('d-block');

    // Enable only MQTT inputs
    mqtt.querySelectorAll('input, select, textarea').forEach(function (input) {
        input.disabled = false;
    });
    mqttCustom.querySelectorAll('input, select, textarea').forEach(function (input) {
        input.disabled = true;
    });
    http.querySelectorAll('input, select, textarea').forEach(function (input) {
        input.disabled = true;
    });
    httpCustom.querySelectorAll('input, select, textarea').forEach(function (input) {
        input.disabled = true;
    });
}

function showMqttCustomSection() {
    var mqtt = document.getElementById('mqtt');
    var mqttCustom = document.getElementById('mqttCustom');
    var http = document.getElementById('http');
    var httpCustom = document.getElementById('httpCustom');

    // Show only MQTT Custom section
    mqttCustom.classList.remove('d-none');
    mqttCustom.classList.add('d-block');

    // Hide other sections
    mqtt.classList.add('d-none');
    mqtt.classList.remove('d-block');
    http.classList.add('d-none');
    http.classList.remove('d-block');
    httpCustom.classList.add('d-none');
    httpCustom.classList.remove('d-block');

    // Enable only MQTT Custom inputs
    mqtt.querySelectorAll('input, select, textarea').forEach(function (input) {
        input.disabled = true;
    });
    mqttCustom.querySelectorAll('input, select, textarea').forEach(function (input) {
        input.disabled = false;
    });
    http.querySelectorAll('input, select, textarea').forEach(function (input) {
        input.disabled = true;
    });
    httpCustom.querySelectorAll('input, select, textarea').forEach(function (input) {
        input.disabled = true;
    });
}

function showHttpSection() {
    var mqtt = document.getElementById('mqtt');
    var mqttCustom = document.getElementById('mqttCustom');
    var http = document.getElementById('http');
    var httpCustom = document.getElementById('httpCustom');

    // Show only HTTP section
    http.classList.remove('d-none');
    http.classList.add('d-block');

    // Hide other sections
    mqtt.classList.add('d-none');
    mqtt.classList.remove('d-block');
    mqttCustom.classList.add('d-none');
    mqttCustom.classList.remove('d-block');
    httpCustom.classList.add('d-none');
    httpCustom.classList.remove('d-block');

    // Enable only HTTP inputs
    http.querySelectorAll('input, select, textarea').forEach(function (input) {
        input.disabled = false;
    });
    mqtt.querySelectorAll('input, select, textarea').forEach(function (input) {
        input.disabled = true;
    });
    mqttCustom.querySelectorAll('input, select, textarea').forEach(function (input) {
        input.disabled = true;
    });
    httpCustom.querySelectorAll('input, select, textarea').forEach(function (input) {
        input.disabled = true;
    });
}

function showHttpCustomSection() {
    var mqtt = document.getElementById('mqtt');
    var mqttCustom = document.getElementById('mqttCustom');
    var http = document.getElementById('http');
    var httpCustom = document.getElementById('httpCustom');

    // Show only HTTP Custom section
    httpCustom.classList.remove('d-none');
    httpCustom.classList.add('d-block');

    // Hide other sections
    mqtt.classList.add('d-none');
    mqtt.classList.remove('d-block');
    mqttCustom.classList.add('d-none');
    mqttCustom.classList.remove('d-block');
    http.classList.add('d-none');
    http.classList.remove('d-block');

    // Enable only HTTP Custom inputs
    httpCustom.querySelectorAll('input, select, textarea').forEach(function (input) {
        input.disabled = false;
    });
    mqtt.querySelectorAll('input, select, textarea').forEach(function (input) {
        input.disabled = true;
    });
    mqttCustom.querySelectorAll('input, select, textarea').forEach(function (input) {
        input.disabled = true;
    });
    http.querySelectorAll('input, select, textarea').forEach(function (input) {
        input.disabled = true;
    });
}

function handleEndpointTypeChange(endpointType) {
    if (endpointType.value === 'mqtt') {
        showMqttSection();
    } else if (endpointType.value === 'mqttCustom') {
        showMqttCustomSection();
    } else if (endpointType.value === 'http') {
        showHttpSection();
    } else if (endpointType.value === 'httpCustom') {
        showHttpCustomSection();
    }
}

document.addEventListener('DOMContentLoaded', function () {
    var endpointType = document.getElementById('id_endpoint_type');

    // Run appropriate function on page load
    handleEndpointTypeChange(endpointType);

    // Attach change event listener to dropdown
    endpointType.addEventListener('change', function () {
        handleEndpointTypeChange(this);
    });
});

// Handle back/forward navigation using the pageshow event
window.addEventListener('pageshow', function () {
    var endpointType = document.getElementById('id_endpoint_type');
    handleEndpointTypeChange(endpointType);
});
