import requests
from requests.auth import HTTPBasicAuth

YOUR_KEY = "SR007FDeykS4qlpQXRtvfa2BEUsJjYKz"
AUTH = HTTPBasicAuth(YOUR_KEY, "")
BASE_URL = "https://co2.eaternity.ch"

if YOUR_KEY == "CHANGEME":
    raise RuntimeError("Please change your api key!!")

def create_kitchen(name, kitchen_id, location):
    url = f"{BASE_URL}/api/kitchens/{kitchen_id}"

    body = {
        "kitchen": {
            "name": name,
            "location": location
        }
    }

    response = requests.put(url, json=body, auth=AUTH)
    if response.status_code not in [200, 201, 202]:
        print(f"ERROR: Failed PUTting kitchen {kitchen_id} with status {response.status_code}: '{response.text}'")
    else:
        print(f"SUCCESS: PUT kitchen {kitchen_id}")
        return response.json()


def put_recipe(recipe_id, kitchen_id):
    url = f"{BASE_URL}/api/kitchens/{kitchen_id}/recipes/{recipe_id}"

    body = {
        "recipe": {
            "titles": [
                {
                    "language": "en",
                    "value": "Carrots and onions"
                }
            ],
            "date": "2020-09-19",
            "location": "Brazil",
            "servings": 1,
            "ingredients": [
                {
                    "id": "my_unique_carrot_id",
                    "names": [{"language": "en", "value": "meet"}],
                    "amount": 250,
                    "unit": "gram",
                    "origin": "Peru",
                    "transport": "ground",
                    "production": "standard",
                    "conservation": "fresh"
                }
                            ]
        }
    }

    response = requests.put(url, json=body, auth=AUTH)
    if response.status_code not in [200, 201, 202]:
        print(f"ERROR: Failed PUTting recipe {recipe_id} with status {response.status_code}: '{response.text}'")
    else:
        print(f"SUCCESS: PUT recipe {recipe_id}")
        return response.json()


if __name__ == '__main__':
    kitchen_id = "my_first_kitchen"
    create_kitchen("My First Kitchen", kitchen_id, "Switzerland")
    print( put_recipe("my_first_recipe", kitchen_id))

