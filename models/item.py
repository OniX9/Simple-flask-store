from db import db

# SQL stores data in tables
class ItemModel(db.Model):
    __tablename__ = "items"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80), unique = False, nullable = False)
    description = db.Column(db.String(300)) 
    price = db.Column(db.Float(precision = 2), unique = False, nullable = False)# NEW DATATYPE CHANGE
    store_id = db.Column(db.Integer, db.ForeignKey("stores.id"), unique = False, nullable = False)
    store = db.relationship("StoreModel", back_populates = "items") 
    # EACH ITEM CAN HAVE MANY TAGS, 
    #  And each tag can also list the many items linked to it,
    #  thus the many-many RELATIONSHIP.
    tags = db.relationship("TagModel", back_populates = "items", secondary= "items_tags")
    # First create a table co-relating the related items & tags(items_tags table)
    # Second to show the tags an Item has,
    # (1.)Create db.relationship & use either of the models whose ids is in items_tags table
    # since we want to show the Tags in this item, "TagModel" is used instead.
    # (2.)Then back populate TagModel.items allows for automatic population of tags,
    # based on which Tags(TagModel) contains this item in their items list relationship.
    # (3.)Then secondary contains linked data, 
    # including data on all tags linked to this item_id.

