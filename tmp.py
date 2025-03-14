import os
import sys
import requests


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
    Calls the Nutritionix API to fetch nutritional details for the given ingredients query.
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

    payload = {"query": ingredients_query}

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code != 200:
        print("Error: Failed to retrieve data from Nutritionix API.")
        print("Response:", response.text)
        sys.exit(1)

    return response.json()


def calculate_totals(nutrition_data):
    """
    Sums up nutritional values from all food items returned by the Nutritionix API.
    """
    fields = [
        "nf_calories",
        "nf_total_fat",
        "nf_saturated_fat",
        "nf_cholesterol",
        "nf_sodium",
        "nf_total_carbohydrate",
        "nf_dietary_fiber",
        "nf_sugars",
        "nf_protein",
        "nf_potassium",
    ]

    totals = {field: 0.0 for field in fields}

    foods = nutrition_data.get("foods", [])
    for food in foods:
        for field in fields:
            totals[field] += food.get(field, 0)

    return totals


def print_totals(totals):
    """
    Prints the aggregated nutritional information.
    """
    print("\nTotal Nutritional Information:")
    for key, value in totals.items():
        print(f"{key}: {value}")


def main():
    # Get ingredients in German from the user.
    ingredients_german = input(
        "Geben Sie Ihre Zutatenliste ein (z.B. '2 Eier, 1 Tasse Milch, 1 Scheibe Brot'): "
    )

    # Translate the German ingredients list to English.
    ingredients_english = translate_to_english(ingredients_german)
    print("\nTranslated Ingredients:", ingredients_english)

    # Retrieve nutritional data using the translated text.
    nutrition_data = get_nutrition_info(ingredients_english)

    # Calculate total nutritional values.
    totals = calculate_totals(nutrition_data)

    # Print the aggregated nutritional information.
    print_totals(totals)


if __name__ == "__main__":
    main()
