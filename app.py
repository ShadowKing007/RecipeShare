from flask import Flask, render_template
import sqlite3
import json

app = Flask(__name__,template_folder='templates')
# Serve static files (CSS, JS, images, etc.) from the 'static' folder
app.static_folder = 'static'

@app.route('/')
def index():
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
    # Close the database connection
    conn.commit()
    conn.close()

    return render_template('index.html', recipes_data=recipes_data)

if __name__ == '__main__':
    app.run(debug=True)
