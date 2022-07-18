const attrForm = document.getElementsByClassName("d_attr_form");
const mainForm = document.querySelector("#form-container");
const addButton = document.querySelector("#add-form");
const emptyForm = document.querySelector("#empty_form");

let formCount = attrForm.length - 1;

addButton.addEventListener("click", function (event) {
    event.preventDefault();
    const newAttrForm = emptyForm.cloneNode(true);

    formCount++;

    newAttrForm.innerHTML = newAttrForm.innerHTML.replace(/__prefix__/g, formCount);

    let newAttrFormToInsert = document.createElement('div');
    newAttrFormToInsert.classList.add('d_attr_form', 'col-6');

    let innerAttrForm = document.createElement('form');
    innerAttrForm.method = 'POST';
    innerAttrForm.append(...newAttrForm.childNodes);

    let innerAttrButton = document.createElement('button');
    innerAttrButton.classList.add('remove-form', 'btn', 'btn-danger', 'rounded-pill', 'btn-sm');
    innerAttrButton.innerHTML = "<i class='bi bi-trash'></i>";
    newAttrFormToInsert.append(innerAttrForm, innerAttrButton);

    mainForm.append(newAttrFormToInsert);

    let removeChildButton = newAttrFormToInsert.querySelector('.remove-form');
    removeChildButton.addEventListener("click", function () {
        if(removeChildButton.parentElement.className === "d_attr_form col-6"){
            removeChildButton.parentElement.remove();
        }
    })

});


let removeButton = document.querySelectorAll(".remove-form");
removeButton.forEach(function (elem) {
    elem.addEventListener("click", function () {
        if(elem.parentElement.className === "d_attr_form col-6"){
            elem.parentElement.remove();
        }
    });
});