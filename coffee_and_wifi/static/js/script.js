document.querySelectorAll("form .form-control").forEach(element => {
    element.addEventListener("focus", () => {
        const notifications = document.querySelector(".notifications");
        if (notifications) {
            notifications.remove();
        }
    });
})