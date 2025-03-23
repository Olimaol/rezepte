import json
import os
from jinja2 import Environment, FileSystemLoader
import requests
import sys


def translate_to_english(text):
    """
    Translates the provided German text into English using the DeepL API.

    Requirements:
    - Set the environment variable DEEPL_API_KEY with your DeepL API key.

    For production use, DeepL (or Google Cloud Translation) is recommended for its accuracy and reliability.
    """
    deepL_api_key = os.environ.get("DEEPL_API_KEY")
    if not deepL_api_key:
        print("Error: Please set DEEPL_API_KEY in your environment.")
        sys.exit(1)

    url = "https://api-free.deepl.com/v2/translate"
    payload = {
        "auth_key": deepL_api_key,
        "text": text,
        "source_lang": "DE",  # Specify source language as German.
        "target_lang": "EN",  # Translate to English.
    }

    response = requests.post(url, data=payload)
    if response.status_code != 200:
        print("Error: Failed to translate text with DeepL API.")
        print("Response:", response.text)
        sys.exit(1)

    result = response.json()
    # The API returns a list of translations; we'll use the first one.
    return result["translations"][0]["text"]


def get_nutrition_info(ingredients_query):
    """
    Calls the Nutritionix API to fetch nutritional details
    for a natural language query of ingredients.
    """
    app_id = os.environ.get("NUTRITIONIX_APP_ID")
    api_key = os.environ.get("NUTRITIONIX_API_KEY")

    if not app_id or not api_key:
        print(
            "Error: Please set NUTRITIONIX_APP_ID and NUTRITIONIX_API_KEY in your environment."
        )
        sys.exit(1)

    url = "https://trackapi.nutritionix.com/v2/natural/nutrients"
    headers = {
        "x-app-id": app_id,
        "x-app-key": api_key,
        "Content-Type": "application/json",
    }

    # The query field should contain the ingredients list.
    payload = {"query": ingredients_query}

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code != 200:
        print("Error: Failed to retrieve data from Nutritionix API.")
        print("Response:", response.text)
        sys.exit(1)

    return response.json()


def calculate_totals(nutrition_data):
    """
    Sums the nutritional values across all food items returned by the API.
    """
    # Define the nutritional fields we're interested in.
    fields = [
        "nf_calories",
        "nf_total_fat",
        "nf_saturated_fat",
        # "nf_cholesterol",
        # "nf_sodium",
        "nf_total_carbohydrate",
        # "nf_dietary_fiber",
        "nf_sugars",
        "nf_protein",
        # "nf_potassium",
    ]

    totals = {field: 0.0 for field in fields}

    foods = nutrition_data.get("foods", [])
    for food in foods:
        for field in fields:
            val = food.get(field, 0.0)
            val = val if val is not None else 0.0
            totals[field] += val

    # round the totals to two decimal places
    totals = {field: round(value, 2) for field, value in totals.items()}

    # transform the values to strings and add units

    return totals


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
    # Query nutritional info using all ingredients as a single query
    ingredients_german = " ".join(recipe["ingredients"])
    try:
        ingredients_english = translate_to_english(ingredients_german)
        nutrition_data = get_nutrition_info(ingredients_english)
        nutrition_totals = calculate_totals(nutrition_data)
    except Exception:
        nutrition_totals = None
    output_path = os.path.join(output_dir, f"{index}.html")
    with open(output_path, "w", encoding="utf-8") as output_file:
        # Pass index as additional variable for the template.
        output_file.write(
            template.render(recipe=recipe, nutrition=nutrition_totals, index=index)
        )

# Generate index.html
index_template = env.get_template("index_template.html")
with open("index.html", "w", encoding="utf-8") as index_file:
    index_file.write(index_template.render(recipes=recipes))
