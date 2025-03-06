from flask import Flask, render_template, request
import requests

app = Flask(__name__)

api_key = "e5e736aaa7mshc2faf4686c2451fp13b4a7jsne8890789e1e1"
url = "https://keto-diet.p.rapidapi.com/"

headers = {
    "X-RapidAPI-Key": api_key,
    "X-RapidAPI-Host": "keto-diet.p.rapidapi.com"
}

@app.route('/', methods=['GET', 'POST'])
def index():
    recipe_details = None
    error = None
    if request.method == 'POST':
        recipe_name = request.form['recipe'].strip()
        response = requests.get(url, headers=headers)

        if response.status_code == 200:  
            data = response.json()

            
            if isinstance(data, list):
                recipe = next((r for r in data if r['recipe'].lower() == recipe_name.lower()), None)

                if recipe:
                    recipe_details = {
                        "recipe": recipe['recipe'],
                        "prep_time_in_minutes": recipe['prep_time_in_minutes'],
                        "difficulty": recipe['difficulty'],
                        "serving": recipe['serving'],
                        "ingredients": [
                            recipe['ingredient_1'],
                            recipe['ingredient_2'],
                            recipe['ingredient_3'],
                            recipe['ingredient_4'],
                            recipe['ingredient_5']
                        ],
                        "directions": [
                            recipe['directions_step_1'],
                            recipe['directions_step_2'],
                            recipe['directions_step_3'],
                            recipe['directions_step_4'],
                            recipe['directions_step_5']
                        ],
                        "image": recipe['image'],
                        "calories": recipe['calories'],
                        "fat": recipe['fat_in_grams'],
                        "carbohydrates": recipe['carbohydrates_in_grams'],
                        "protein": recipe['protein_in_grams']
                    }
                else:
                    error = f"No recipe found with name: {recipe_name}"
            else:
                error = "Unexpected API response structure. Please check the API response."
        else:
            error = f"Failed to fetch data from API. Status code: {response.status_code}"

    return render_template('index.html', recipe=recipe_details, error=error)

if __name__ == '__main__':
    app.run()
