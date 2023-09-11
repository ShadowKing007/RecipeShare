from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash
import sqlite3
import json
import os
from sqlite3 import Cursor
app = Flask(__name__, static_url_path='/static',template_folder='templates')
# Serve static files (CSS, JS, images, etc.) from the 'static' folder
app.static_folder = 'static'

app.secret_key = os.urandom(24)
# Fake user data (replace this with a real user database)
users = {'user1': 'password1', 'user2': 'password2'}
@app.route('/')
def index():
    if 'logged_in' in session and session['logged_in']:
        return home()
    else:
        return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in users and users[username] == password:
            session['logged_in'] = True
            session['username'] = username
            return redirect(url_for('index'))
        else:
            flash('Incorrect username or password. Please try again.', 'error')
            return render_template('login.html')
    else:
        return render_template('login.html')

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/home')
def home():
    # Connect to the SQLite database
    conn = sqlite3.connect('myrecipe.db')
    cursor = conn.cursor()

    # Read the JSON data from a file (replace 'recipes.json' with your JSON file path)
    with open('recipes1.json', 'r', encoding='utf-8') as json_file:
        recipes_data = json.load(json_file)


    # Define the table schema (assuming a 'recipes' table)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS recipes (
        RecipeID INTEGER PRIMARY KEY,
        TranslatedRecipeName TEXT,
        TranslatedIngredients TEXT,
        TotalTimeInMins INTEGER,
        Cuisine TEXT,
        TranslatedInstructions TEXT,
        URL TEXT,
        CleanedIngredients TEXT,
        ImageURL TEXT,
        IngredientCount INTEGER
    )
''')

# Insert each recipe from the JSON data into the table
    for recipe in recipes_data:
        cursor.execute('''
        INSERT INTO recipes (
            TranslatedRecipeName,
            TranslatedIngredients,
            TotalTimeInMins,
            Cuisine,
            TranslatedInstructions,
            URL,
            CleanedIngredients,
            ImageURL,
            IngredientCount
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        recipe['TranslatedRecipeName'],
        recipe['TranslatedIngredients'],
        recipe['TotalTimeInMins'],
        recipe['Cuisine'],
        recipe['TranslatedInstructions'],
        recipe['URL'],
        recipe['Cleaned-Ingredients'],
        recipe['image_url'],
        recipe['Ingredient-count']
    ))  
    # Fetch data from the 'recipes' table
    num_recipes_to_display = 30  # Number of recipes to display
    recipes_to_display = recipes_data[:num_recipes_to_display]

    # Close the database connection
    conn.commit()
    conn.close()

    return render_template('index.html', recipes_data=recipes_to_display)

#searching of recipes

@app.route('/search')
def search_recipe():
    query = request.args.get('q')
    print(f'Searching for: {query}')
    app.logger.info(f"Received query: {query}")
    conn = sqlite3.connect('myrecipe.db')
    cursor = conn.cursor()
    # Perform a database query based on the search query
    cursor.execute("SELECT DISTINCT TranslatedRecipeName, ImageURL, TranslatedIngredients, TotalTimeInMins, Cuisine, TranslatedInstructions, URL, CleanedIngredients, IngredientCount FROM recipes WHERE TranslatedRecipeName LIKE ? LIMIT 30", ('%' + query + '%',))

    results = cursor.fetchall()

    # Convert the results to a list of dictionaries
    recipes = []
    for (
        TranslatedRecipeName, ImageURL, TranslatedIngredients,
        TotalTimeInMins, Cuisine, TranslatedInstructions, URL,
        CleanedIngredients, IngredientCount
    ) in results:
        recipe = {
            'name': TranslatedRecipeName,
            'image_url': ImageURL,
            'ingredients': TranslatedIngredients,
            'total_time': TotalTimeInMins,
            'cuisine': Cuisine,
            'instructions': TranslatedInstructions,
            'url': URL,
            'cleaned_ingredients': CleanedIngredients,
            'ingredient_count': IngredientCount,
        }
        recipes.append(recipe)

    app.logger.info(f"Found {len(recipes)} matching recipes")

    return jsonify(recipes)
@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)

