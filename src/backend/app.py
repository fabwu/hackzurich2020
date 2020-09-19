from flask import Flask
import recipe_matching
import eaternity

app = Flask(__name__)

@app.route('/recipe/<query>')
def get_score_for_recipe(query):
    '''
    :param query: POST BASE/score
        [
            "Red Thai Curry",
            "Spaghetti Carbonara"
        ]
    :return:
    '''
    print(f"Request for recipe {query}")

    recipe, http_code = recipe_matching.find_matching_recipe(query, 'de')
    ingredients = recipe['ingredients']
    if http_code != 200:
        return http_code

    scores = eaternity.get_score(ingredients)

    return {
        'query': query,
        'scores': scores
    }