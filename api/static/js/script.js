document.addEventListener("DOMContentLoaded", async function () {
    const response = await fetch("/api/films");
    
    if (response.ok) {
        const films = await response.json();
        const filmsList = document.getElementById("films-list");

        // Vider la liste avant d'y ajouter les films
        filmsList.innerHTML = "";

        // Pour chaque film, créer un élément <li> et l'ajouter à la liste
        films.forEach(film => {
            const li = document.createElement("li");
            
            // Créer un élément pour l'image
            const img = document.createElement("img");
            img.src = film.image;  // URL de l'image
            img.alt = film.title;  // Texte alternatif
            img.width = 100;  // Taille de l'image

            // Ajouter le contenu : titre, année, résumé
            const title = document.createElement("h2");
            title.textContent = `${film.title} (${film.year})`;

            const summary = document.createElement("p");
            summary.textContent = film.summary;

            // Ajouter les éléments dans <li>
            li.appendChild(img);
            li.appendChild(title);
            li.appendChild(summary);
            
            // Ajouter <li> à la liste <ul>
            filmsList.appendChild(li);
        });
    } else {
        console.error("Erreur lors de la récupération des films");
    }
});
