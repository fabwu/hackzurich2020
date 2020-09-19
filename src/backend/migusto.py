from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
from elasticsearch_dsl.connections import connections

BASE_URL = "https://hackzurich-api.migros.ch/hack/recipe/recipes_de/_search"

connections.create_connection(hosts=[BASE_URL],http_auth=('hackzurich2020','uhSyJ08KexKn4ZFS'))

s = Search().query("match", title="Suppe")   

response = s.execute()


for hit in response:
    print(hit.meta.score, hit.title)