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
        if not success:
            return {}, 500

        if not recipe:
            queries.append({
                'query': dish,
                'matched-recipe': 'Not Found',
                'matched-ingredients': [],
                'indicators': [],
            })
        else:
            ingredients = recipe['ingredients']
            indicators = eaternity.get_indicators(ingredients)
            queries.append({
                'query': dish,
                'matched-recipe': recipe['title'],
                'matched-ingredients': ingredients,
                'indicators': indicators,
            })

    return {
        'queries': queries
    }
