# Hack Zurich

## Links

- https://www.ibm.com/blogs/digitale-perspektive/2020/09/hackzurich-2020-ibm-swiss-re/
- https://lemon-pebble-032061603.azurestaticapps.net/home

## Run Backend

```
# Switch to venv
pip install requests flask goslate

export FLASK_APP=src/backend/app.py
export FLASK_ENV=development
python -m flask run
```