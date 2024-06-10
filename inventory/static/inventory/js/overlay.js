document.addEventListener("DOMContentLoaded", function() {
    var statusField = document.getElementById("id_status");
    var overlay = document.getElementById("overlay");
    var overlayText = document.getElementById("overlay-text");

    if (statusField && overlay && overlayText) {
        statusField.addEventListener("change", function() {
            if (statusField.value === "received") {
                overlay.style.display = "block"; // Show the overlay
                overlayText.innerText = "Complete"; // Set the watermark text
            } else {
                overlay.style.display = "none"; // Hide the overlay for other statuses
            }
        });
    }
});