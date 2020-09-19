
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

    textinput_words = [w for w in word_tokenize(textinput) if len(w) > 1]
    if len(textinput_words) == 0:
        raise ValueError("please input words with more than one letter") ## return error code instead?

    # detect if language is English (remove if takes long)
    if lang is None:  # detect if english
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


    '''POST "hack/recipe/recipes_de/_search"  \
           -H "Content-Type: application/json"  \
           -d '{"query": {"match": {"title":{"query":"Spanferkel"}}}}'
    '''

    json_query = '{"query": {"match": {"title":{"query":"'+urllib.parse.quote(textinput)+'"}}}}' #
    '{"query": {"match": {"title":{"query":"Spanferkel"}}}}'
    headers = {'Content-Type': 'application/json'}
    req = requests.post(BASE_URL + f"hack/recipe/recipes_{lang}/_search", data=json_query, auth=AUTH, headers=headers)
    assert req.status_code == 200, f"Error: {req.status_code}, {req.content}"



def testme():
    textinput = "Spaghetti Carbonara"
    find_matching_recipe(textinput, lang="de")

if __name__ == '__main__':
    testme()