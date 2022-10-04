var deleteModal = document.getElementById('deleteModal')
if (deleteModal) {
    deleteModal.addEventListener('show.bs.modal', function (event) {
        // Button that triggered the modal
        var button = event.relatedTarget
        // Extract info from data-bs-* attribute
        var url = button.getAttribute('data-bs-url')

        var modalForm = deleteModal.querySelector('.modal-form')
        modalForm.attributes.getNamedItem('action').value = url
    })
}
