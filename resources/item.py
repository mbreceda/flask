import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import items

blp = Blueprint("Items", __name__, description="Operations on items")

@blp.route('/item/<string:item_id>')
class Item(MethodView):
    def get(self, item_id):
        try: 
            return items[item_id]
        except KeyError: 
            abort(404, message="Item not found")
    
    def delete(self, item_id):
        try:
            del items[item_id]
            return { "message": "Item deleted" }
        except KeyError:
            abort(404, message="Item not found")

    def put(self, item_id):
        item_data = request.get_json()
        if "prince" not in item_data or "name" not in item_data:
            abort(400, message="Missing required fields")

        try:
            item = items[item_id]
            item |= item_data
            return item
        except KeyError:
            abort(404, message="Item not found")


@blp.route('/item')
class ItemList(MethodView):
    def get(self):
        return { "items": list(items.values()) }

    def post(self):
        item_data = request.get_json()
        if (
            "price" not in item_data 
            or "name" not in item_data
            or "store_id" not in item_data
        ): 
            abort(400, message="Missing required fields")

        for item in items.values():
            if item["name"] == item_data["name"]:
                abort(400, message="Item already exists")
        item_id = uuid.uuid4().hex
        item = {**item_data, "id": item_id }
        items[item_id] = item
        return item, 201
    