htmx.on("htmx:afterSwap", (e) => {
    // Response targeting #dialog => show the modal
    if (e.detail.target.id == "div_entities") {
        updateRemoveListeners();
    }
})

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
