import json
from flask import Flask, render_template, request

app = Flask(__name__)
app.config['SECRET_KEY'] = 'an insanely secret and long key'


def get_entities():
    with open('entities.json') as f:
        return json.load(f)


ENTITIES = get_entities()


@app.route('/')
def index():
    return render_template("main-all-items.html", entities=ENTITIES)


@app.route('/paging/<int:page>')
def paging(page):

    return render_template("page.html", entities=ENTITIES, page=page)


@app.route('/search')
# поиск по 1-му слову
# def search():
#     model = request.args.get('model')
#     response = ENTITIES if not model else [e for e in ENTITIES if e["model"] == model]
#     return render_template("search_ause.html", entities=response)
# поиск по 2-м словам
# model = request.args.get('model')
# response = []
# if model:
#     model = ' '.join(model.strip().lower().split())
#     response = [e for e in ENTITIES if e["model"] == model]
#     if not response:
#         model_lst = model.split()
#         response = [e for e in ENTITIES if model_lst[0] in e["model"].split()]
#         if (len(model_lst) > 1) and not response:
#             response = [e for e in ENTITIES if model_lst[1] in e["model"].split()]
# return render_template("search_ause.html", entities=response)
# универсальный поиск - любое количество слов, разделенных пробелом
def search():
    model = request.args.get('model')
    response = []
    if model:
        model = ' '.join(model.strip().lower().split())  # removing excess spaces
        response = [e for e in ENTITIES if e["model"] == model]
        if not response:
            model_lst = model.split()
            for word in model_lst:
                response = [e for e in ENTITIES if word in e["model"].split()]
                if response:
                    break
    return render_template("search_ause.html", entities=response)


@app.route('/card/<int:eid>')
def card(eid: int):
    for ent in ENTITIES:
        if ent["id"] == eid:
            return render_template("card_full.html", entity=ent)
    return "<h1>No such a card</h1>"


@app.route('/card_short/<int:eid>')
def card_short(eid: int):
    for ent in ENTITIES:
        if ent["id"] == eid:
            return render_template("card_short.html", entity=ent)
    return "<h1>No such a card</h1>"


if __name__ == '__main__':
    app.run(debug=True)
