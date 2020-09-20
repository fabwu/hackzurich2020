# Hack Zurich

Foodprint is an app that helps you assess the environmental footprint of different meal options when scanning a menu in a restaurant.

This is our submission to HackZurich 2020.

## Links

- https://www.ibm.com/blogs/digitale-perspektive/2020/09/hackzurich-2020-ibm-swiss-re/
- https://lemon-pebble-032061603.azurestaticapps.net/home

## Run Backend

```
# Switch to venv
pip install requests flask goslate


export FLASK_APP=src/backend/application.py
export FLASK_ENV=development
python -m flask run
```

## Deployment

```
az webapp up
```
