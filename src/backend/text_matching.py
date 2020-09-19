

from Levenshtein import distance as levenshtein_distance, editops as levenshtein_editops
import random
import re

def find_best_match(search_str, options):
    '''
    :param search_str:
    :param options: a list of strings, with options to match to
    :return: (match, close_enough)
        match: the best matching string from :param options
        close_enough: boolean whether it's a close match or not
    '''
    options_lc = [o.lower() for o in options]
    search_str.lower() in options_lc
    distances = {}
    is_subset = {}
    for opt in options:
        dist = levenshtein_distance(search_str.lower(), opt.lower())
        distances[opt] = dist
        # if (search_str.lower() in opt.lower() ) or (opt.lower() in search_str.lower()):
        if (opt.lower() in search_str.lower()):
            is_subset[opt] = True

    min_dist = min(distances.values())
    min_dist_opts = [key for key, val in distances.items() if val == min_dist]


    close_enough = False
    if len(search_str) *0.3 > min_dist:
        close_enough = True
        if len(min_dist_opts) > 1:
            pass
            # print("Check whether all of the results are valid anyway. Then we can pick one.")
    elif len(is_subset) > 0:
        # It seems to happen often that the Migros ingredients are longer strings that contain the shorter eaternity
        #   string as substring. It's not completely accurate (e.g. Kalbsschnitzel gets matched to Kalb, not to Kalb (Schnitzel).
        distances = {key: val for key, val in distances.items() if key in is_subset}
        min_dist = min(distances.values())
        min_dist_opts = [key for key, val in distances.items() if val == min_dist]
        close_enough = True

    best_match = random.choice(min_dist_opts)
    best_match = best_match.strip(".;") # "Buchweizen" in the document has a comma after it...
    return best_match, close_enough

    # print(options)