;(function () {
  const modal = new bootstrap.Modal(document.getElementById("m_general"))

  htmx.on("htmx:afterSwap", (e) => {
    // Response targeting #dialog => show the modal
    if (e.detail.target.id == "dg_general") {
      modal.show()
    }
  })

  htmx.on("htmx:beforeSwap", (e) => {
    // Empty response targeting #dialog => hide the modal
    if (e.detail.target.id == "dg_general" && !e.detail.xhr.response) {
      modal.hide()
      e.detail.shouldSwap = false
    }
  })

  // Remove dialog content after hiding
  htmx.on("hidden.bs.modal", () => {
    document.getElementById("dg_general").innerHTML = ""
  })
})()
