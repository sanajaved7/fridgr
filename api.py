from flask import Flask, jsonify
from db import Items
our_fridge = Items()


app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/fridge")
def fridge():
    fridge_list = []

    for item in our_fridge.get_fridge_items():
        fridge_list.append({'name': item[0], 'fridge': item[1], 'grocery': item[2], 'date': item[3], 'quantity': item[4]})


    return jsonify({"fridge": fridge_list})

@app.route("/fridge/<name>")
def fridge_item(name):
    item = our_fridge.get_one_item(name)
    return jsonify({'name': item[0], 'fridge': item[1], 'grocery': item[2], 'date': item[3], 'quantity': item[4]})


if __name__ == "__main__":
    app.run()
