
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
    :return: tbd, probably a dict or a json representing a single recipe that matches best
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

    # all returned recipe names - it only returns 10
    names = [h['_source']['title'] for h in req.json()['hits']['hits'] ]

    # This one is Spaghetti Carbonara (in testing):
    carbonara = req.json()['hits']['hits'][42]


def testme():
    textinput = "Spaghetti Carbonara"
    find_matching_recipe(textinput, lang="de")

if __name__ == '__main__':
    testme()