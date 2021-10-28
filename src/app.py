from typing import List
from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)

api = Api(app)

items: List = []


class Item(Resource):
    def get(self, name):
        for item in items:
            if item['name'] == name:
                return item
        return {'item': None}, 404

    def post(self, name):
        item = {'name': name, "price": 12}
        items.append(item)
        return item, 201


class ItemList(Resource):
    def get(self):
        return {'items': items}

api.add_resource(Item, '/items/<string:name>')
api.add_resource(ItemList, '/items')

app.run(port=3333, debug=True)
