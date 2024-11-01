# Schemas are used for validation, in this case is validating:
# data that can only be sent by server, (dump_on1y=True)
#  bcos it's created by server i.e: UUID for created object,
#  loads_only is the reverse.
# data that are required from client (required=True),
# optional data from client, &
# data type that should be provided by client.
from marshmallow import Schema, fields

# ITEMS
class PlainItemSchema(Schema):
    id = fields.Integer(dump_only= True)
    name = fields.Str(required= True)
    price = fields.Float(required= True)

class PlainStoreSchema(Schema):
    id = fields.Integer(dump_only= True)
    name = fields.Str(required = True)

class PlainTagSchema(Schema):
    id = fields.Integer(dump_only = True)
    name = fields.Str(required= True)

class ItemSchema(PlainItemSchema): 
    # Inherits PlainItemSchema & it's arguments,
    #   it also helps in the segementation of args based on usage,
    #   especially to avoid recursion.
    store_id = fields.Integer(required= True, load_only= True)
    store = fields.Nested(PlainStoreSchema(), dump_only = True)
    tags = fields.List(fields.Nested(PlainTagSchema()), dump_only =True)
    # fields.Nested allows assigning of another shema in store var,
    #  just like when a child dict is nested in one of the parent dict's key.

class ItemUpdateSchema(Schema):
    id = fields.Integer(dump_only= True)
    # Supposed to be dump_only, but put request can now create an item
    # Although in resources.item the logic would only set name 
    store_id = fields.Integer() 
    name = fields.Str(required= False)
    price = fields.Float(required= False)
    # tags = fields.List(fields.Nested(PlainTagSchema()), dump_only =True)


class StoreSchema(PlainStoreSchema):
    items = fields.List(fields.Nested(PlainItemSchema()), dump_only = True)
    tags = fields.List(fields.Nested(PlainTagSchema()), dump_only= True)

class TagSchema(PlainTagSchema):
    store_id = fields.Integer(loads_only = True)
    store= fields.Nested(PlainStoreSchema(), dump_only = True)
    items = fields.List(fields.Nested(PlainItemSchema()), dump_only =True)

class TagAndItemSchema(Schema):
    message = fields.Str(dump_only= True)
    items = fields.Nested(ItemSchema)
    tags = fields.Nested(TagSchema)

class UserSchema(Schema):
    id = fields.Int(dump_only = True)
    username = fields.Str(required= True)
    password = fields.Str(required=  True, load_only = True)