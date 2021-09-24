import json

from flask import Flask, render_template, request

app = Flask(__name__)


def get_entities():
    with open('entities.json') as f:
        return json.load(f)


ENTITIES = get_entities()


@app.route('/')
def index():
    return render_template("main-all-items.html", entities=ENTITIES)


@app.route('/paging')
def paging():
    return render_template("main.html")


@app.route('/search')
def search():
    model = request.args.get('model')
    response = []
    if not model:
        response = ENTITIES
    else:
        for e in ENTITIES:
            if e["model"] == model:
                response.append(e)
    return render_template("search_ause.html", entities=response)


@app.route('/card/<int:eid>')
def card(eid: int):
    for ent in ENTITIES:
        if ent["id"] == eid:
            return render_template("card_full.html", entity=ent)


if __name__ == '__main__':
    app.run(debug=True)
