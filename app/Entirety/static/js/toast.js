window.toastElement = window.toastElement || document.getElementById("toast");
window.toastBody = window.toastBody || document.getElementById("toast-body");

window.toast = window.toast || new bootstrap.Toast(window.toastElement, { delay: 2000 });


htmx.on("showMessage", (e) => {
  window.toastBody.innerText = e.detail.value;
  window.toast.show();
});

