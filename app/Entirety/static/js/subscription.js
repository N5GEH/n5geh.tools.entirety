// ;(function () {
//     let addButton = document.querySelectorAll(".add-entity");
//
//     addButton.forEach(function (elem) {
//         elem.addEventListener("click", function (event) {
//             event.preventDefault();
//             let emptyForm = document.querySelector('.empty-form')
//             let mainForm = document.querySelector('.form-container')
//
//             const newEntityForm = emptyForm.cloneNode(true);
//
//             // probably there's a more elegant way
//             let prefix = emptyForm.querySelector('fieldset').querySelector('div').getAttribute("id").split("-")[0].split("_").pop();
//             let totalForms = document.getElementById('id_' + prefix + '-TOTAL_FORMS');
//             let formCount = parseInt(totalForms.value);
//
//             newEntityForm.innerHTML = newEntityForm.innerHTML.replace(/__prefix__/g, formCount);
//             mainForm.append(...newEntityForm.childNodes);
//             totalForms.value = formCount + 1;
//
//             updateRemoveListeners();
//         });
//     });
//
//     updateRemoveListeners();
// })()
//
//

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

    let emptyForm = document.querySelector('.empty-form')

    let prefix = emptyForm.querySelector('fieldset').querySelector('div').getAttribute("id").split("-")[0].split("_").pop();
    let totalForms = document.getElementById('id_' + prefix + '-TOTAL_FORMS');
    let formCount = parseInt(totalForms.value);

    totalForms.value = formCount - 1;

    let elem = event.currentTarget;
    if (elem.parentElement.classList.contains("entity-form")) {
        elem.parentElement.remove();
    }
}
