let addButton = document.querySelectorAll(".add-form");
addButton.forEach(function (elem) {
    elem.addEventListener("click", function (event) {
        event.preventDefault();
        sibling = elem.parentElement.parentElement.parentElement.children
        for(node in sibling) {
            if(sibling[node].classList){
                if (sibling[node].classList.contains('empty_form')) {
                emptyForm = sibling[node];
            }
            if (sibling[node].classList.contains('form-container')) {
                mainForm = sibling[node];
            }
            }

        }
        const newAttrForm = emptyForm.cloneNode(true);
        let prefix = emptyForm.firstElementChild.getAttribute("id").split("-")[0].split("_").pop();
        let totalForms = document.getElementById('id_' + prefix + '-TOTAL_FORMS');
        let formCount = parseInt(totalForms.value)

        newAttrForm.innerHTML = newAttrForm.innerHTML.replace(/__prefix__/g, formCount);

        let newAttrFormToInsert = document.createElement('div');
        newAttrFormToInsert.classList.add('d_attr_form', 'col-6');

        let innerAttrButton = document.createElement('button');
        innerAttrButton.classList.add('remove-form', 'btn', 'btn-danger', 'rounded-pill', 'btn-sm');
        innerAttrButton.innerHTML = "<i class='bi bi-trash'></i>";
        newAttrFormToInsert.append(...newAttrForm.childNodes, innerAttrButton);

        addTooltipEvent(newAttrFormToInsert);

        mainForm.append(newAttrFormToInsert);
        totalForms.setAttribute('value', (formCount + 1).toString())

        let removeChildButton = newAttrFormToInsert.querySelector('.remove-form');
        removeChildButton.addEventListener("click", function () {
            if (removeChildButton.parentElement.className === "d_attr_form col-6") {
                removeChildButton.parentElement.remove();
            }
        })
    })
});

function addTooltipEvent(elems) {
    var tooltipTriggerList = elems.querySelectorAll('[data-bs-toggle="tooltip"]');
    tooltipTriggerList.forEach(function (elem) {
        bootstrap.Tooltip.getOrCreateInstance(elem, {title:elem.getAttribute('aria-label')})
    })

}

let removeButton = document.querySelectorAll(".remove-form");
removeButton.forEach(function (elem) {
    elem.addEventListener("click", function () {
        if(elem.parentElement.className === "d_attr_form col-6"){
            elem.parentElement.remove();
        }
    });
});
