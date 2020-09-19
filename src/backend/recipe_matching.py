import requests
from requests.auth import HTTPBasicAuth
import re

BASE_URL = "https://hackzurich-api.migros.ch/"

USER = "hackzurich2020"
PASSWORD = "uhSyJ08KexKn4ZFS"
AUTH = HTTPBasicAuth(USER, PASSWORD)

ALL_UNITS = [
    'g',
    'Bund',
    'dl',
    'l',
    # Todo
]
KNOWN_UNITS = ["g", "l", "dl", "kg"]

def word_tokenize(text):
    parsed = re.split(" |-", text )
    parsed = [re.sub('[\W_]+', '', w) for w in parsed]
    return parsed

def migusto_to_eaternity_unit(unit_name, amount, ingredient_id=None):
    ''''''
    if (amount == 0) or (unit_name not in KNOWN_UNITS):
        if ingredient_id is not None:
            # Todo: Can use the ingredients API and find out the type? -> lower weight for spices
            raise NotImplementedError
        # unit is _not_ required, according to the docs -- edit: but then it defaults to gram. Not useful.
        unit_name = "gram"
        amount = 250
    else:
        if unit_name in ["g", "l"]:
            unit_name = "gram" if unit_name == "g" else "liter"
        elif unit_name == "dl":
            unit_name = "liter"
            amount *= 0.1
        elif unit_name == "kg":
            unit_name = "gram"
            amount *= 1000
        else:
            raise NotImplementedError("Todo, unit: "+unit_name)
    return unit_name, amount


LANGUAGE_MAP = {'en': 'english', 'fr': 'french', 'it': 'italian', 'de': 'german'}

def simplify_ingredient_name(ingredient_description, lang):
    import spacy
    assert lang is not None
    ingred_words = word_tokenize(ingredient_description, language=LANGUAGE_MAP[lang])

    nlp = spacy.load(lang)
    doc = nlp(ingredient_description)
    sub_toks = [tok for tok in doc if (tok.dep_ == "ROOT")]

    import nltk
    tags = nltk.pos_tag(ingred_words)
    # We keep all kinds of words, and foreign words
    ingred_words = [ingred for i, ingred in enumerate(ingred_words) if (tags[i][1].startswith('NN') or tags[i][1] =='FW')]
    print("breakp")



def find_matching_recipe(textinput, lang=None):
    '''
    :param textinput: a list of strings. if lang=None, detect if english, else assume german.
                    To specify language: english: lang="en", french: lang="fr", german: lang="de",italian: "it".
    :return: A list of dictionaries. Each dict represents the best matching recipe for one search input,
            it has information about ingredients for one portion, ie one person:
        {
         "title": ...,
         "nutrients": [dict of nutrients for one portion],
         "ingredients": {
            'name': string with name, possibly more specifiers (eg. "in oil"),
            'lang': "fr", "it" or "de"
            'unit': eg. "gram" , will be (todo) same as in eaternity
             # ** Note: unit can be an empty string. This probably always means "piece" or unspecified (eg for salt)
            'quantity': [quantity per portion],
             # ** Note: quantity can be 0 (e.g for "salt" where it's not specified)
           }
         }
         Plus a success boolean, true if a recipe was found

    '''
    # #Returns such a dict
    # return [
    #     {
    #         "name": "Chilli",
    #         "lang": "de",
    #         "amount": 100,
    #         "unit": "gram"
    #     },
    #     {
    #         "name": "Poulet",
    #         "lang": "de",
    #         "amount": 200,
    #         "unit": "gram"
    #     },
    # ], True

    # detect whether language is English, then we'll need to translate

    if lang is None:

        raise NotImplementedError("Please specify a language. NLTK is required for detecting English input.")

        textinput_words_all = [w for w in word_tokenize(" ".join(textinputs)) if len(w) > 1]

        english_vocab = set(w.lower() for w in nltk.corpus.words.words())
        text_vocab = set(w.lower() for w in textinput_words_all if w.lower().isalpha())
        unusual = text_vocab.difference(english_vocab)

        if len(unusual) < 0.5 * len(textinput_words_all):  # if more than half the words are in english
            lang = "en"
        else:
            lang = "de"

    textinput_word = word_tokenize(textinput)

    if len(textinput_word) == 0:
        raise ValueError("please input at least one word with more than one letter. Input was: "+str(textinput)) ## return error code instead?

    if lang == "en":
        # translate
        import goslate
        gs = goslate.Goslate()
        textinput_en = textinput
        # This works, BUT this calls an API with a rate limit. I think it's one request per 3 seconds... not good.
        textinput = " ".join(list(gs.translate(textinput_word, 'de')))
        lang = "de"

    # recipe search
    data  = {
        "query": {
            "simple_query_string": {
                "query": textinput,
            }
        }
    }
    req = requests.post(f"{BASE_URL}hack/recipe/recipes_{lang}/_search",
                        json=data, auth=AUTH, headers={'Content-Type': 'application/json'})

    assert req.status_code == 200, f"Error: {req.status_code}, {req.content}"

    recipes = req.json()['hits']['hits']

    if len(recipes) == 0:
        return [], 404
    # # ... Todo
    #
    # # all returned recipe names - it only returns 10
    # names = [h['_source']['title'] for h in recipes ]
    #
    # # ... Todo

    best_match = recipes[0]["_source"] # preliminary


    # Get ingredients with quantities
    num_portions =  best_match["sizes"][0]["quantity"]
    ingredients_dict_blocks = best_match["sizes"][0]["ingredient_blocks"]
    for ingredients_dicts in ingredients_dict_blocks:
        # assert len(ingredients_dicts) == 1, "Rewrite to handle all blocks of ingredients"
        ingredients_dicts = ingredients_dicts["ingredients"]

        ingredients = []
        for ing in ingredients_dicts:
            # name = simplify_ingredient_name(ing['text'], lang=lang)
            name = ing['text']
            if len(name.split(" ")) > 1:
                # skip ingredients with more than one word to minimize things eaternity does not recognize
                # continue
                pass
            ingred =  { #'id': ing['id'],
                    'name': name,
                    'lang': lang
            }
            unit, amount = migusto_to_eaternity_unit(
                    ing['amount']['unit'] ,
                    ing['amount']['quantity'] / num_portions
            )
            ingred['amount'] = amount
            # Unit is not required, according to the docs
            if unit is not None:
                ingred['unit'] = unit

            ingredients.append(ingred)

    result_dict = { "title": best_match["title"],
                    "nutrients": best_match["nutrients"],
                    "ingredients": ingredients
                    }

    return result_dict, 200


def testme():
    textinputs = [
"Red-Thai-Curry",
"Spaghetti-carbonara",
"Caesar-Salad",
"Wiener-Schnitzel"
]
    textinput = textinputs[2]
    find_matching_recipe(textinput, lang="de") # "en")

if __name__ == '__main__':
    testme()