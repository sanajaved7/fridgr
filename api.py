from flask import Flask, jsonify, request
from db import Items
import datetime
our_fridge = Items()


app = Flask(__name__)


@app.route("/", methods=['GET'])
def hello():
    return "Hello and welcome to your personal fridge app! :D"

@app.route("/fridge", methods=['GET', 'POST'])
def fridge():
    """Returns all the items in the fridge"""
    if request.method == 'GET':
        fridge_list = []
        for row in our_fridge.get_fridge_items():
            fridge_list.append(our_fridge.row_to_dict(row))
        return jsonify({"fridge": fridge_list})
    elif request.method = 'POST':
        name = request.form['name'],
        quantity = request.form['quantity']
        our_fridge.add_item(name=name, fridge=1, grocery=0, date=datetime.date.today(), quantity=quantity)


@app.route("/grocery", methods=['GET', 'POST'])
def grocery():
    """Returns all items on our grocery list"""
    if request.method == 'GET':
        grocery_list = []
        for row in our_fridge.get_grocery_items():
            grocery_list.append(our_fridge.row_to_dict(row))
        return jsonify({"grocery": grocery_list})
    elif request.method == 'POST':
        name = request.form['name'],
        quantity = request.form['quantity']
        our_fridge.add_item(name=name, fridge=0, grocery=1, date=datetime.date.today(), quantity=quantity)


@app.route("/items/<name>", methods=['GET', 'DELETE'])
def fridge_item(name):
    """Returns one item info from the fridge"""
    if request.method == 'GET':
        row = our_fridge.get_one_item(name)
        return jsonify(our_fridge.row_to_dict(row))
    elif request.method == 'DELETE':
        our_fridge.delete_item(name=name)

@app.route("")

if __name__ == "__main__":
    app.run()
