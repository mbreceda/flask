from marshmallow import Schema, fields


class ItemSchema(Schema):
    id = fields.Str(dump_default=True)
    name = fields.Str(required=True)
    price = fields.Float(required=True)
    store_id = fields.Str(required=True)


class ItemUplodateSchema(Schema):
    name = fields.Str()
    price = fields.Float()


class StoreSchema(Schema):
    id = fields.Str(dump_default=True)
    name = fields.Str(required=True)





