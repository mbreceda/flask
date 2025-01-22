import uuid
from flask import Flask, request
from flask_smorest import abort
from db import items, stores

app = Flask(__name__)


@app.get("/store")
def get_store():
    return { "stores": list(stores.values()) }


@app.get("/store/<string:store_id>")
def get_store_by_id(store_id):
    try: 
        return stores[store_id]
    except KeyError: 
        abort(404, message="Store not found")


@app.post('/store')
def create_store():
    store_data = request.get_json()
    if "name" not in store_data:
        abort(400, message="Missing required fields")

    for store in stores.values():
        if store["name"] == store_data["name"]:
            abort(400, message="Store already exists")

    store_id = uuid.uuid4().hex
    store = {**store_data, "id": store_id }
    stores[store_id] = store
    return store, 201

@app.delete('/store/<string:store_id>')
def delete_item(store_id):
    try:
        del stores[store_id]
        return { "message": "Store deleted" }
    except KeyError:
        abort(404, message="Store not found")

# ITEMS

@app.post('/item')
def create_item():
    item_data = request.get_json()
    if (
        "price" not in item_data 
        or "name" not in item_data
        or "store_id" not in item_data
    ): 
        abort(400, message="Missing required fields")

    for item in item.values():
        if item["name"] == item_data["name"]:
            abort(400, message="Item already exists")

    store_id = item_data["store_id"]
    if item_data[store_id] not in stores:
        abort(404, message="Store not found")
    
    item_id = uuid.uuid4().hex
    item = {**item_data, "id": item_id }
    items[item_id] = item
    return item, 201


@app.get('/item')
def get_all_items():
    return { "items": list(items.values()) }


@app.get('/item/<string:item_id>')
def get_item_by_id(item_id):
    try:
        return items[item_id]
    except KeyError:
        abort(404, message="Item not found")
    

@app.delete('/item/<string:item_id>')
def delete_item(item_id):
    try:
        del items[item_id]
        return { "message": "Item deleted" }
    except KeyError:
        abort(404, message="Item not found")
    
    
@app.put('/item/<string:item_id>')
def update_item(item_id):
    item_data = request.get_json()
    if "prince" not in item_data or "name" not in item_data:
        abort(400, message="Missing required fields")

    try:
        item = items[item_id]
        item |= item_data
        return item
    except KeyError:
        abort(404, message="Item not found")
 