document.getElementById("login-form").addEventListener("submit", async function (event) {
    event.preventDefault();
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    const response = await fetch("/login/", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded"
        },
        body: new URLSearchParams({
            "username": username,
            "password": password
        })
    });

    if (response.ok) {
        window.location.href = "/";  // Redirige vers la page d'accueil
    } else {
        document.getElementById("error-message").textContent = "Échec de la connexion.";
    }
});

document.getElementById("register-form").addEventListener("submit", async function (event) {
    event.preventDefault();
    const name = document.getElementById("reg-name").value;
    const username = document.getElementById("reg-username").value;
    const password = document.getElementById("reg-password").value;

    const response = await fetch("/register/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            "name": name,
            "email": username,
            "password": password
        })
    });

    if (response.ok) {
        document.getElementById("error-message").textContent = "Compte créé avec succès, veuillez vous connecter.";
    } else {
        document.getElementById("error-message").textContent = "Erreur lors de la création du compte.";
    }
});

