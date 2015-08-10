from flask import Flask, jsonify
from db import Items
our_fridge = Items()


app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World!"


@app.route("/fridge")
def fridge():
    """Returns all the items in the fridge"""
    fridge_list = []
    for row in our_fridge.get_fridge_items():
        fridge_list.append(our_fridge.row_to_dict(row))
    return jsonify({"fridge": fridge_list})


@app.route("/fridge/<name>")
def fridge_item(name):
    """Returns one item info from the fridge"""
    row = our_fridge.get_one_item(name)
    return jsonify(our_fridge.row_to_dict(row))


@app.route("/grocery")
def grocery():
    """Returns all items on our grocery list"""
    grocery_list = []
    for row in our_fridge.get_grocery_items():
        grocery_list.append(our_fridge.row_to_dict(row))
    return jsonify({"grocery": grocery_list})

@app.route("")

if __name__ == "__main__":
    app.run()
