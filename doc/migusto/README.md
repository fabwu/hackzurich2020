Website: https://lemon-pebble-032061603.azurestaticapps.net/data

# API Cred

HTTP Basic

Username: hackzurich2020
Password: uhSyJ08KexKn4ZFS

# Migusto Doc

Try this:

* Searching for reciptes with "Spanferkel" in the title

        curl -X POST "https://hackzurich-api.migros.ch/hack/recipe/recipes_de/_search"  \
           -H "Content-Type: application/json"  \
           -d '{"query": {"match": {"title":{"query":"Spanferkel"}}}}'

Recipes
-------

Elasticsearch Recipes Database

    GET|POST /hack/recipe/{index:(?:recipes|ingredients|taxonomies|typeahead)_(?:de|fr|it)}/{api:(?:_search|_count)}

Indexes available:

    recipes_de, recipes_fr, recipes_it               actual recipes in the given language
    ingredients_de, ingredients_fr, ingredients_it   ingredients database
    taxonomies_de, taxonomies_fr, taxonomies_it      classification of recipes
    typeahead_de, typeahead_fr, typeahead_it         autocompletion typeahead data 

Only the _search and _count api endpoints of Elasticsearch are exposed.
See https://www.elastic.co/guide/en/elasticsearch/reference/current/search.html
Note: Ingredients map between Products (recipe_ingredient_ids) and the 
Recipes (ingredients.id). E.g. "Zuckerhut" (product id 271380102100) is
ingredient 16318 of recipe 71829 "Zuckerhutsalat mit Kürbis".

Examples:

* Full text query of the German recipes database for "Morcheln" (morels).

        curl "https://hackzurich-api.migros.ch/hack/recipe/recipes_de/_search?q=Morcheln"

* Searching for reciptes with "Spanferkel" in the title

        curl -X POST "https://hackzurich-api.migros.ch/hack/recipe/recipes_de/_search"  \
           -H "Content-Type: application/json"  \
           -d '{"query": {"match": {"title":{"query":"Spanferkel"}}}}'

* Searching recipes containing ingredient 88017 ("Spanferkel"):

        curl -X POST "https://hackzurich-api.migros.ch/hack/recipe/recipes_de/_search"  \
           -H "Content-Type: application/json"  \
           -d '{"query": {"nested":{"path":"ingredients","query": {"term": {"ingredients.id":88017}}}}}'   
