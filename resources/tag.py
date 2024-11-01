from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from db import db
from models import TagModel, StoreModel, ItemModel
from schemas import TagSchema, TagAndItemSchema, ItemSchema

blp = Blueprint("tags", __name__, "operations on tags")


@blp.route("/store/<int:store_id>/tag")
class TagsInStore(MethodView):
    @blp.response(200, TagSchema(many= True))
    def get(self, store_id): # Get tags in store
        store = StoreModel.query.get_or_404(store_id)
        # Using just store.tags won't do, especially as tags is lazy= "dynamic"
        tags = store.tags.all()
        return tags
    
    @blp.arguments(TagSchema)
    @blp.response(201, TagSchema)
    def post(self, tag_data, store_id): # Create Tag
        if TagModel.query.filter(TagModel.store_id == store_id, TagModel.name == tag_data["name"]).first():
            # Checks if Tag name already exists in the particular store.
            # 1st- all Tags with the same id of store_id are filtered,
            # 2nd- all filtered Tags are then checked if their name is same as tag_data["name"],
            # 3rd- The first element of the filter remaining tags list is now returned using .first(),
            # If notthing is returned then Tag name does not exist.
            abort(409, message= "tag already exist in store")
        tag = TagModel(**tag_data, store_id = store_id)
        try:
            db.session.add(tag)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500,  message =  str(e))
        return tag        

@blp.route("/item/<string:item_id>/tag/<string:tag_id>")
class LinkTagstoItem(MethodView):
    @blp.response(201, ItemSchema)
    def post(self,item_id, tag_id):
        tag = TagModel.query.get_or_404(tag_id)
        item = ItemModel.query.get_or_404(item_id)

        if not tag.store_id == item.store_id:
            abort(400, message= "Tag and item store_ids do not match.")
        item.tags.append(tag)
        try:
            db.add(item)
            db.commit()
        except SQLAlchemyError as e:
            abort(500, message= "An error occurred while inserting the tag.")
        return item
    
    def delete(self, item_id, tag_id):
        tag = TagModel.query.get_or_404(tag_id)
        item = ItemModel.query.get_or_404(item_id)
        item.tags.remove(tag)
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message= "An error occurred while unlinking the tag.")
        return {"message": "Item removed from tag", "tag": tag, "item": item}


@blp.route("/tag/<int:tag_id>")
class Tag(MethodView):
    @blp.response(200, TagSchema)
    def get(self, tag_id): #Get tag
        tag = TagModel.query.get_or_404(tag_id)
        return tag
    
    @blp.response(
        202,
        description= "Deletes a tag if no item is tagged with it.",
        example= {"message": "Tag deleted"}
        )
    @blp.response(404, description= "Tag not found.")
    @blp.response(400, description= "Returned if the tag assigned to one or more items. In this case, the tag is not deleted.")
    def delete(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)

        if not tag.items:
            db.session.delete(tag)
            db.session.commit()
            return {"message": "Tag deleted"}
        
        abort(400, message= "Could not delete tag. Make sure tag is not related to any item")