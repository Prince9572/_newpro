document.addEventListener("DOMContentLoaded", function() {
    // Smooth scrolling for navigation links
    const navLinks = document.querySelectorAll("nav ul li a");
    navLinks.forEach(link => {
      link.addEventListener("click", function(e) {
        e.preventDefault();
        const targetId = this.getAttribute("href");
        if (targetId !== "#") {
          document.querySelector(targetId).scrollIntoView({
            behavior: "smooth"
          });
        }
      });
    });
  
    // Explore button scrolls to Gallery section
    const exploreBtn = document.getElementById("exploreBtn");
    if (exploreBtn) {
      exploreBtn.addEventListener("click", function() {
        document.getElementById("gallery").scrollIntoView({
          behavior: "smooth"
        });
      });
    }
  
    // Contact form submission simulation
    const contactForm = document.getElementById("contactForm");
    contactForm.addEventListener("submit", function(e) {
      e.preventDefault();
      // Integrate your AI functionality or API calls here
      alert("Thank you for contacting us! We will get back to you shortly.");
      contactForm.reset();
    });
  });