;(function () {
    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl));

    const url = window.location.pathname;

    const sidebarItems = document.querySelectorAll('.btn-sidebar');
    [...sidebarItems].forEach(el => {
        if(el.getAttribute("href") === url){
            el.classList.add("active")
        }
        else if (!el.classList.contains("hi-ignore")) {
            let regEx = new RegExp(`^${el.getAttribute("href")}.*$`, "i")
            if (regEx.test(url))
                el.classList.add('active')
        }
    })
})()

document.addEventListener('DOMContentLoaded', function() {
    const viewerSearch = document.getElementById('viewerSearch');
    const viewerList = document.getElementById('viewerList');

    viewerSearch.addEventListener('input', function() {
        const query = this.value.toLowerCase();
        const checkboxes = viewerList.querySelectorAll('.form-check');

        checkboxes.forEach(function(checkbox) {
            const label = checkbox.querySelector('label').textContent.toLowerCase();
            if (label.includes(query)) {
                checkbox.style.display = 'block';
            } else {
                checkbox.style.display = 'none';
            }
        });
    });
});

document.addEventListener('DOMContentLoaded', function() {
    const viewerSearch = document.getElementById('userSearch');
    const viewerList = document.getElementById('userList');

    viewerSearch.addEventListener('input', function() {
        const query = this.value.toLowerCase();
        const checkboxes = viewerList.querySelectorAll('.form-check');

        checkboxes.forEach(function(checkbox) {
            const label = checkbox.querySelector('label').textContent.toLowerCase();
            if (label.includes(query)) {
                checkbox.style.display = 'block';
            } else {
                checkbox.style.display = 'none';
            }
        });
    });
});

document.addEventListener('DOMContentLoaded', function() {
    const viewerSearch = document.getElementById('maintainerSearch');
    const viewerList = document.getElementById('maintainerList');

    viewerSearch.addEventListener('input', function() {
        const query = this.value.toLowerCase();
        const checkboxes = viewerList.querySelectorAll('.form-check');

        checkboxes.forEach(function(checkbox) {
            const label = checkbox.querySelector('label').textContent.toLowerCase();
            if (label.includes(query)) {
                checkbox.style.display = 'block';
            } else {
                checkbox.style.display = 'none';
            }
        });
    });
});
