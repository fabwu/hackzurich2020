import requests
import time
import os

from requests.auth import HTTPBasicAuth

YOUR_KEY = "SR007FDeykS4qlpQXRtvfa2BEUsJjYKz"
AUTH = HTTPBasicAuth(YOUR_KEY, "")
BASE_URL = "https://co2.eaternity.ch"
DUMMY_KITCHEN_NAME = 'my_first_kitchen'

if YOUR_KEY == "CHANGEME":
    raise RuntimeError("Please change your api key!!")

PRODUCT_WHITELIST_FILE = 'eaternity_product_list_de.txt'
product_whitelist_de = []

def get_kitchens():
    url = f"{BASE_URL}/api/kitchens/"

    response = requests.get(url, auth=AUTH)

    if response.status_code not in [200, 201, 202]:
        print(
            f"ERROR: Failed GETting kitchen with status {response.status_code}: '{response.text}'")
    else:
        print(f"SUCCESS: GET kitchen")
        return response.json()


def get_all_recipes():
    url = f"{BASE_URL}/api/kitchens/{DUMMY_KITCHEN_NAME}/recipes"

    response = requests.get(url, auth=AUTH)

    if response.status_code not in [200, 201, 202]:
        print(
            f"ERROR: Failed GETting kitchen with status {response.status_code}: '{response.text}'")
    else:
        print(f"SUCCESS: GET kitchen")
        return response.json()


def delete_recipe(recipe_id):
    url = f"{BASE_URL}/api/kitchens/{DUMMY_KITCHEN_NAME}/recipes/{recipe_id}"

    response = requests.delete(url, auth=AUTH)

    if response.status_code not in [204]:
        print(
            f"ERROR: Failed deleting recipe {recipe_id} with status {response.status_code}: '{response.text}'")


def delete_all_recipes():
    """ Removes all recipes (e.g. for cleanup) """

    url = f"{BASE_URL}/api/kitchens/{DUMMY_KITCHEN_NAME}/recipes"

    response = requests.get(url, auth=AUTH)

    if response.status_code not in [200, 201, 202]:
        print(
            f"ERROR: Failed GETting all recipes with status {response.status_code}: '{response.text}'")
    else:
        recipes = response.json()['recipes']

        for recipe_id in recipes:
            delete_recipe(recipe_id)


def get_indicators(ingredients):
    """
    Takes a dict with ingredients and returns environment scores

    [
    {
        "name": "Chilli",
        "lang": "de",
        "amount": 100,
        "unit": "gram"
    },
    {
        "name": "Poulet",
        "lang": "de",
        "amount": 100,
        "unit": "gram"
    },
    ]
    """
    global product_whitelist_de

    if not product_whitelist_de:
        dirname = os.path.dirname(os.path.realpath(__file__))
        with open(f"{dirname}/{PRODUCT_WHITELIST_FILE}") as file:
            product_whitelist_de = [line.strip() for line in file]
            if not product_whitelist_de:
                raise Exception('Whitelist is empty')

    url = f"{BASE_URL}/api/kitchens/{DUMMY_KITCHEN_NAME}/recipes?indicators=true&transient=true"

    req_ingredients = []

    for idx, ing in enumerate(ingredients):
        if ing['name'] not in product_whitelist_de:
            continue

        req_ingredient = {
            # Use new id for each request!!!
            "id": int(time.time()) + idx,
            "type": "conceptual-ingredients",
            "names": [
                {
                    "language": ing['lang'],
                    "value": ing['name']
                }
            ],
            "amount": ing['amount'],
        }

        if 'unit' in ing:
            req_ingredient['unit'] = ing['unit']

        req_ingredients.append(req_ingredient)

    if not req_ingredients:
        raise Exception('No ingredients found for Eaternity') 

    body = {
        "recipe": {
            "location": "Zürich Schweiz",
            "recipe-portions": 1,
            "ingredients": req_ingredients
        }
    }

    response = requests.post(url, json=body, auth=AUTH)
    if response.status_code not in [200, 201, 202]:
        print(
            f"ERROR: Failed creating recipe with status {response.status_code}: '{response.text}'")
    else:
        recipe = response.json()
        # delete recipe as we don't use it
        delete_recipe(recipe['recipe-id'])

        return {
            'co2-eq-in-g': recipe['recipe']['co2-value'],
            'rating': recipe['recipe']['rating']
        }


if __name__ == '__main__':
    # TODO Error handling (what happens if ingredient is not found)
    ingredients = [
        {
            "name": "Chilli",
            "lang": "de",
            "amount": 100,
            "unit": "gram"
        },
        {
            "name": "Poulet",
            "lang": "de",
            "amount": 200,
            "unit": "gram"
        },
    ]

    scores = get_indicators(ingredients)

    print(f"co2 value: {scores['co2-eq-in-g']}g CO₂equivalent")
