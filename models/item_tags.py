from db import db

class ItemTags(db.Model):
    __tablename__ = "items_tags"
    id = db.Column(db.Integer, primary_key = True)
    item_id = db.Column(db.Integer, db.ForeignKey("items.id"), nullable = True)
    tag_id = db.Column(db.Integer, db.ForeignKey("tags.id"), nullable = True)


# items_tags LINK DATA
# id    item_id    tag_id
# 1        2          5
# 2        1          4
# 3        4          5
# 4        1          3

# From the table above, ITEM 1 has both tag 4 & tag 3, 
# while tag 5 has ITEM 2 & 4.
# Then ITEM 2 has only tag 5.