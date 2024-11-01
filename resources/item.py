from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import ItemSchema, ItemUpdateSchema
from models import ItemModel
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from db import db
from flask_jwt_extended import jwt_required, get_jwt

blp = Blueprint("items", __name__, description= "Operations on items")

@blp.route('/item')
class ItemList(MethodView):
    @jwt_required()
    @blp.arguments(ItemSchema)
    @blp.response(200, ItemSchema)
    def post(self, item_data):  # Create new item
        # Assign client's json to the Itemmodel
        # ** assigns  
        # { "name" : "Cup", 
        #     "price" : 500,
        #     "store_id": 1
        # } 
        # to ItemModel(name = "Cup", price = 500, store_id = 500)
        # Note both ItemModel.id & ItemModel.store is automatically generated
        item = ItemModel(**item_data)
        try:
            # Like Git, Add items for SQL Storage,
            # then confirm items Storage with db.session.commit().
            db.session.add(item) 
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message = "An error occur while inserting item")
        return item
    
    @jwt_required()
    @blp.response(200, ItemSchema(many= True))
    def get(self):  # Get all items
        items = ItemModel.query.all()
        return items
    
# from flask_jwt_extended import jwt_required, get_jwt
@blp.route("/item/<string:item_id>")
class Item(MethodView):
    @jwt_required()
    def delete(self, item_id):  # Delete item
        jwt = get_jwt()
        if not jwt.get("is_admin"):
            abort(401, message = "Admin privilege required")
        item = ItemModel.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return {}, 204

    @jwt_required()
    @blp.arguments(ItemUpdateSchema)
    @blp.response(201, ItemUpdateSchema)
    def put(self, item_data, item_id):  # Update item
        # Idempotent request ensures that multiple requests sent by client,
        # results in only one change of state (i.e: in the DB)
        try:
            get_item = ItemModel.query.get(item_id)
            if get_item:
                # Since ItemModel.id is auto-generated make sure to assign the item_id, 
                # so it won't generate a new id & item.
                item = ItemModel(id = item_id, **item_data)
                # .merge method updates only provided client's keys of an existing item,
                # rather than everything.
                db.session.merge(item)
            else:
                # Creates new item_id with item_id, if item already doesn't exist.
                # Also make sure to assign the item_id to ItemModel.id, 
                #   so that multiple request won't generate multiple new items,
                #   rather only 1 item with the specified id is created; making it idempotent.
                item = ItemModel(id = item_id, **item_data)
                db.session.add(item)
            db.session.commit()
        except IntegrityError:
               abort(400, message = 'name, price & store_id has to be included when creating a new item')
        return get_item
    
    @jwt_required()
    @blp.response(200, ItemSchema)
    def get(self, item_id):  # Get item
        # item = ItemModel.query.get(item_id) #GET METHOD
        # using .get_or_404 instead would return a 404, 
        # if item with item_id does not exist
        item = ItemModel.query.get_or_404(item_id)
        print("Item:", item)
        return item
    
