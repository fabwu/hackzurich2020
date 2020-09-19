'''
        Ignore this file for now.
'''


import requests, json
from requests.auth import HTTPBasicAuth
import urllib.parse


BASE_URL = "https://hackzurich-api.migros.ch/"

USER = "hackzurich2020"
PASSWORD = "uhSyJ08KexKn4ZFS"
AUTH = HTTPBasicAuth(USER, PASSWORD)

OUTPUT_BASE = "sample_ingredients_"

def build_ingredient_list():
    '''
        Reads a lot of ingredients from the API, and then stores them as reference material (for word frequencies)

    :return:
    '''

    for lang in ["fr", "de", "it"]:
        all_ingredient_names = set()
        for i in range(100):
            # 100*100 = 10'000 recipes to parse
            params = {"size": 100, "from": 100*i}
            headers = {'Content-Type': 'application/json'}
            req = requests.get(BASE_URL + f"hack/recipe/recipes_{lang}/_search",
                               params=params, auth=AUTH, headers=headers)

            if req.status_code != 200:
                print(f"Error: {req.status_code}, {req.content}")
                continue
                # assert req.status_code == 200, f"Error: {req.status_code}, {req.content}"

            recipes = req.json()['hits']['hits']
            for r in recipes:
                ingreds = r["_source"]["sizes"][0]["ingredient_blocks"][0]["ingredients"] # meh
                names = [ing['text'] for ing in ingreds]
                all_ingredient_names = all_ingredient_names.union(set(names))

        print(f"Found {len(all_ingredient_names)} ingredients, without duplicates")

        with open(OUTPUT_BASE + lang + ".txt", 'w') as fd:
            for name in all_ingredient_names:
                fd.write(name + "\n")
            # fd.writelines(list(all_ingredient_names))
        print(f"Stored all found {lang} ingredients to file "+OUTPUT_BASE + lang + ".txt")


if __name__ == '__main__':
    build_ingredient_list()