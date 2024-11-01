import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import abort, Blueprint
from schemas import StoreSchema
from db import db
from models import StoreModel
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from flask_jwt_extended import jwt_required

blp = Blueprint('stores', __name__, description= "Operations on stores")

@blp.route("/store/<int:store_id>")
class Store(MethodView):
    @blp.response(200, StoreSchema)
    def get(self, store_id):  # Get store
        store = StoreModel.query.get_or_404(store_id)
        print("Store:", store)
        return store

    jwt_required(fresh= True)
    def delete(self, store_id):  #Delete store  
        store = StoreModel.query.get_or_404(store_id)
        db.session.delete(store)
        db.session.commit()
        return {}, 204


@blp.route("/store")
class StoreList(MethodView):
    @blp.arguments(StoreSchema)
    @blp.response(200, StoreSchema)
    def post(self, store_data):  # Create new store
        # Assign client's json to the StoreModel
        # ** assigns  
        # { 
        #   "name" : "Samsung"
        # } 
        # to StoreModel(name = "Samsung")
        # Note both StoreModel.id & StoreModel.items is automatically generated
        store = StoreModel(**store_data)
        try:
            db.session.add(store)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message= 'An error occur while inserting store')
        except IntegrityError:
            # IntegrityError is thrown, when any of the data been saved to DB would 
            # violates the constraints set by us.
            # In this case store name isn't unique.
            abort(400, message= 'A store with that name already exist')
        return store
    
    @blp.response(200, StoreSchema(many= True))
    def get(self):  # Get all stores
        stores = StoreModel.query.all()
        return stores
    