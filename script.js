const eventDropdown = document.getElementById("event");
const feeDisplay = document.getElementById("feeDisplay");

const registrationForm = document.getElementById("registrationForm");
const statusMessage = document.getElementById("statusMessage");

const nameInput = document.getElementById("name");
const emailInput = document.getElementById("email");


// Display registration fee when event is selected
eventDropdown.addEventListener("change", function () {

    if (eventDropdown.value === "coding") {
        feeDisplay.textContent = "Registration Fee: 200 INR";
    }
    else if (eventDropdown.value === "hackathon") {
        feeDisplay.textContent = "Registration Fee: 500 INR";
    }
    else if (eventDropdown.value === "robotics") {
        feeDisplay.textContent = "Registration Fee: 300 INR";
    }
    else {
        feeDisplay.textContent = "";
    }

});


// Submit event listener
registrationForm.addEventListener("submit", function (event) {

    // Prevent page refresh
    event.preventDefault();

    // Validate all fields
    if (
        nameInput.value.trim() === "" ||
        emailInput.value.trim() === "" ||
        eventDropdown.value === ""
    ) {
        statusMessage.textContent = "Please fill all fields.";
        return;
    }

    // Successful registration
    statusMessage.textContent = "Registration submitted successfully!";

});