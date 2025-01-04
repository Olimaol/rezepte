const recipeContainer = document.getElementById('recipe-list');

const recipes = [
    { title: 'Einfaches Pfannkuchen-Rezept', file: '../recipes/recipe1.html', image: '../images/image.png' },
    { title: 'Recipe 2', file: '../recipes/recipe2.html', image: '../images/image.png' },
    { title: 'Recipe 3', file: '../recipes/recipe3.html', image: '../images/image.png' }
];

function displayRecipes() {
    recipes.forEach(recipe => {
        const recipeElement = document.createElement('div');
        recipeElement.classList.add('w3-card-4', 'w3-margin', 'w3-hover-shadow'); // w3-css classes
        recipeElement.onclick = () => window.location.href = recipe.file;

        const contentElement = document.createElement('div');
        contentElement.classList.add('w3-container');

        const titleElement = document.createElement('h2');
        titleElement.textContent = recipe.title;
        titleElement.classList.add('w3-text-teal');

        contentElement.appendChild(titleElement);

        const imageElement = document.createElement('div');
        imageElement.classList.add('w3-container');

        const img = document.createElement('img');
        img.src = recipe.image;
        img.alt = recipe.title;
        img.classList.add('w3-image', 'w3-round');

        imageElement.appendChild(img);

        recipeElement.appendChild(contentElement);
        recipeElement.appendChild(imageElement);
        recipeContainer.appendChild(recipeElement);
    });
}

document.addEventListener('DOMContentLoaded', displayRecipes);