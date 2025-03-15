function toggleMenu() {
    document.getElementById("nav-links").classList.toggle("show");
  }
  
  function toggleFeedbackForm() {
    var formContainer = document.getElementById("feedback-form-container");
  
    if (formContainer.classList.contains("hidden")) {
      formContainer.classList.remove("hidden");
      formContainer.classList.add("visible");
    } else {
      formContainer.classList.remove("visible");
      formContainer.classList.add("hidden");
    }
  }
  