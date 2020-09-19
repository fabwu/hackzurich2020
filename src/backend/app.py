from flask import Flask
import recipe_matching
import eaternity

app = Flask(__name__)

@app.route('/recipe/<query>')
def get_score_for_recipe(query):
    print(f"Request for recipe {query}")

    ingredients = recipe_matching.find_matching_recipe(query, 'de')

    scores = eaternity.get_score(ingredients)

    return {
        'query': query,
        'scores': scores
    }