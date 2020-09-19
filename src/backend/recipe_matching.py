
import requests, json
from requests.auth import HTTPBasicAuth
import urllib.parse
import nltk
from nltk.tokenize import word_tokenize


BASE_URL = "https://hackzurich-api.migros.ch/"

USER = "hackzurich2020"
PASSWORD = "uhSyJ08KexKn4ZFS"
AUTH = HTTPBasicAuth(USER, PASSWORD)

def find_matching_recipe(textinput, lang=None):
    '''
    :param textinput: a string. if lang=None, detect if english, else assume german.
                    To specify language: english: lang="en", french: lang="fr", german: lang="de",italian: "it".
    :return: A dictionary representing the best matching recipe:
        {
         "title": ...,
         "portions": 1, [always],
         "nutrients": [dict of nutrients for one portion],
         "ingredients": {
            'id': migusto-id,
            'name': string with name, possibly more specifiers (eg. "in oil"),
            'unit': eg. "g" for gram
             # ** Note: unit can be an empty string. This probably always means "piece" or unspecified (eg for salt)
            'quantity': ing['amount']['quantity'] / num_portions,
             # ** Note: quantity can be 0 (e.g for "salt" where it's not specified)
           }
         }

    '''

    #TODO return such a dict
    return [
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

    textinput_words = [w for w in word_tokenize(textinput) if len(w) > 1]

    if len(textinput_words) == 0:
        raise ValueError("please input words with more than one letter") ## return error code instead?

    # detect if language is English
    if lang is None:
        english_vocab = set(w.lower() for w in nltk.corpus.words.words())
        text_vocab = set(w.lower() for w in textinput_words if w.lower().isalpha())
        unusual = text_vocab.difference(english_vocab)
        if len(unusual) < 0.5 * len(textinput_words): # if more than half the words are in english
            lang = "en"

    if lang == "en":
        # translate
        import goslate
        gs = goslate.Goslate()
        textinput_en = textinput
        textinput = gs.translate(textinput, 'de', 'en')
        lang = "de"

    # recipe search

    params = {"q": urllib.parse.quote(textinput), "size":100}
    headers = {'Content-Type': 'application/json'}
    req = requests.get(BASE_URL + f"hack/recipe/recipes_{lang}/_search",
                       params=params, auth=AUTH, headers=headers)

    assert req.status_code == 200, f"Error: {req.status_code}, {req.content}"

    recipes = req.json()['hits']['hits']
    # ... Todo

    # all returned recipe names - it only returns 10
    names = [h['_source']['title'] for h in recipes ]

    # This one is Spaghetti Carbonara (in testing):
    carbonara = recipes[42]

    # ... Todo
    best_match = recipes[0]["_source"] # preliminary

    # Get ingredients with quantities
    num_portions =  best_match["sizes"][0]["quantity"]
    ingredients_dicts = best_match["sizes"][0]["ingredient_blocks"]
    assert len(ingredients_dicts) == 1, "Rewrite to handle all blocks of ingredients"
    ingredients_dicts = ingredients_dicts[0]["ingredients"]

    ingredients = []
    for ing in ingredients_dicts:
        ingredients.append(
            {'id': ing['id'],
             'name': ing['text'],
             'unit': ing['amount']['unit'],  # Note: unit can be an empty string, probably always means "piece" or unspecified (eg salt)
             'quantity': ing['amount']['quantity'] / num_portions,  # Note: quantity can be 0 (e.g for "salt" where it's not specified)
             }
        )

    result_dict = {"title": best_match["title"],
                   "portions": 1,
                   "nutrients": best_match["nutrients"],
                   "ingredients": ingredients
                   }
    return result_dict


def testme():
    textinput = "Spaghetti Carbonara"
    find_matching_recipe(textinput, lang="de")

if __name__ == '__main__':
    testme()