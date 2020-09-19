from flask import Flask, request
app = Flask(__name__)
import recipe_matching
import eaternity

@app.route('/score', methods=['POST'])
def get_score():
    queries = []
    dishes = request.get_json(force=True)

    for dish in dishes:
        recipe, success = recipe_matching.find_matching_recipe(dish, 'de')
        ingredients = recipe['ingredients']
        if not success:
            return 404



        indicators = eaternity.get_indicators(ingredients)

        queries.append({
            'query': dish,
            'indicators': indicators
        })


    return {
        'queries': queries
    }

@app.route('/recipe/<query>')
def get_score_for_recipe(query):
    print(f"Request for recipe {query}")

    recipe, success = recipe_matching.find_matching_recipe(query, 'de')
    ingredients = recipe['ingredients']
    if not success:
        return 404

    scores = eaternity.get_score(ingredients)

    return {
        'query': query,
        'scores': 113
    }
