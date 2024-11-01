from db import db

class StoreModel(db.Model):
    __tablename__ = "stores" 
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80), nullable = False, unique = True)
    # EACH STORE CAN HAVE MANY ITEMS & TAGS UNDER IT, 
    #  So in items & tags, 1 relationship btw the them(item and tags) & the store, 
    #  meaning each item/ tag has only 1 store it is linked to, 
    #  while a store can have many items & tags related to it.Thus 1-many RELATIONSHIP.
    items = db.relationship("ItemModel", back_populates = "store", lazy= "dynamic")
    # The code above has several items(ItemModel) been populated in the
    # items variable above automaically,
    # based on if their ForeignKey <store_id> matches this stores.id
    # lazy= "dynamic" means items won't load unless it is been called
    tags = db.relationship("TagModel", back_populates = "store", lazy = "dynamic")
    
