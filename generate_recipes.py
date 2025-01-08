import json
import os
from jinja2 import Environment, FileSystemLoader

# Load recipes from JSON file
with open("recipes/recipes.json", "r", encoding="utf-8") as file:
    recipes = json.load(file)

# Set up Jinja2 environment
env = Environment(
    loader=FileSystemLoader(".")
)  # Change the loader path to the current directory
template = env.get_template("recipes/recipe-template.html")

# Create output directory if it doesn't exist
output_dir = "recipes/"
os.makedirs(output_dir, exist_ok=True)

# Generate HTML files for each recipe
for index, recipe in enumerate(recipes):
    output_path = os.path.join(output_dir, f"{index}.html")
    with open(output_path, "w", encoding="utf-8") as output_file:
        output_file.write(template.render(recipe=recipe))

# Generate index.html
index_template = env.get_template("index_template.html")
with open("index.html", "w", encoding="utf-8") as index_file:
    index_file.write(index_template.render(recipes=recipes))
