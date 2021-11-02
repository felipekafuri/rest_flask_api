from typing import List
from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt_extended import jwt_required, JWTManager, create_access_token, get_jwt_identity

from security import authenticate, identity

app = Flask(__name__)
app.secret_key = 'felipe'

api = Api(app)

jwt = JWTManager(app)  # /auth

items: List = []


class Authentication(Resource):
    def post(self):
        data = request.get_json()
        username = data['username']
        password = data['password']
        authUser = authenticate(username, password)
        return {'token': create_access_token(identity=authUser)}


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    @jwt_required()
    def get(self, name):
        # give us the first item in the list
        item = next(filter(lambda x: x['name'] == name, items), None)
        return {'item': item}, 200 if item else 404

    def post(self, name):
        if next(filter(lambda x: x['name'] == name, items), None) is not None:
            return {'message': 'An item with name {} already exists.'.format(name)}, 400
        
        data = Item.parser.parse_args()

        item = {'name': name, "price": data['price']}
        items.append(item)
        return item, 201

    def delete(self, name):
        global items
        items = list(filter(lambda x: x['name'] != name, items))
        return {'message': 'Item deleted'}

    def put(self, name):
        data = Item.parser.parse_args()

        item = next(filter(lambda x: x['name'] == name, items), None)
        if item is None:
            item = {'name': name, 'price': data['price']}
            items.append(item)
        else:
            item.update(data)
        return item


class ItemList(Resource):
    def get(self):
        return {'items': items}


api.add_resource(Authentication, '/auth')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')

app.run(port=3333, debug=True)
