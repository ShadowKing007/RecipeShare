// Function to fetch and display search results

function searchRecipes(query) {
    fetch(`/search?q=${query}`)
        .then(response => response.json())
        .then(data => {
            // Assuming you have a container element where you want to display the recipes
            const resultsContainer = document.getElementById('results');
            resultsContainer.innerHTML = ''; // Clear previous results
            if (data.length === 0) {
                resultsContainer.innerHTML = '<p>No matching recipes found.</p>';
            } else {
                data.forEach(recipe => {
                    // Create a container for each recipe
                    const recipeDiv = document.createElement('div');
                    recipeDiv.classList.add('recipe-grid'); // Apply CSS styles for your grid here

                    // Create elements for each piece of recipe data
                    const img = document.createElement('img');
                    img.src = recipe.image_url;
                    img.alt = recipe.name;

                    const heading = document.createElement('h2');
                    heading.textContent = recipe.name;

                    const ingredients = document.createElement('p');
                    ingredients.innerHTML = `<strong>Ingredients:</strong> ${recipe.ingredients}`;

                    const totalTime = document.createElement('p');
                    totalTime.innerHTML = `<strong>Total Time:</strong> ${recipe.total_time} mins`;

                    const cuisine = document.createElement('p');
                    cuisine.innerHTML = `<strong>Cuisine:</strong> ${recipe.cuisine}`;

                    const instructions = document.createElement('p');
                    instructions.innerHTML = `<strong>Instructions:</strong> ${recipe.instructions}`;

                    const url = document.createElement('p');
                    url.innerHTML = `<strong>URL:</strong> <a href="${recipe.url}">${recipe.url}</a>`;

                    const ingredientCount = document.createElement('p');
                    ingredientCount.innerHTML = `<strong>Total Ingredients:</strong> ${recipe.ingredient_count}`;

                    // Append elements to the recipe container
                    recipeDiv.appendChild(img);
                    recipeDiv.appendChild(heading);
                    recipeDiv.appendChild(ingredients);
                    recipeDiv.appendChild(totalTime);
                    recipeDiv.appendChild(cuisine);
                    recipeDiv.appendChild(instructions);
                    recipeDiv.appendChild(url);
                    recipeDiv.appendChild(ingredientCount);

                    // Append the recipe container to the results container
                    resultsContainer.appendChild(recipeDiv);
                });
            }

        })
        .catch(error => console.error('Error:', error));
}

// Wait for the DOM to be fully loaded before attaching the event listener
document.addEventListener('DOMContentLoaded', function () {
    // Handle form submission
    const searchForm = document.getElementById('search-form');
    searchForm.addEventListener('submit', function (event) {
        event.preventDefault();
        const searchInput = document.getElementById('search-input');
        const query = searchInput.value.trim();
        if (query !== '') {
            searchRecipes(query);
        }
    });
});
const searchButton = document.getElementById('search-button');
const loadingScreen = document.getElementById('loading-screen');

// Function to show the loading screen
function showLoadingScreen() {
    loadingScreen.style.display = 'flex'; // Show the loading screen
}

// Function to hide the loading screen
function hideLoadingScreen() {
    loadingScreen.style.display = 'none'; // Hide the loading screen
}

// Event listener for the search button click
searchButton.addEventListener('click', () => {
    // Show the loading screen when the search button is clicked
    showLoadingScreen();

    async function fetchRecipeData() {
        try {
            const response = await fetch('/search_recipe'); // Replace with your API endpoint or data source URL
            const data = await response.json();
            return data;
        } catch (error) {
            console.error('Error:', error);
        }
    }
    
    setTimeout(() => {
        // After the operation is complete, hide the loading screen
        hideLoadingScreen();

        // Display the search results or perform other actions here
    }, 10000); // Adjust the timeout duration as needed
});


