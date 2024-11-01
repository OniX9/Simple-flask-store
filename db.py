from flask_sqlalchemy import SQLAlchemy

# create an SQLAlchemy instance(i.e db)
db = SQLAlchemy()



# class DataBase: #Schema inheritance representation as dictionary
#     items:dict[str, dict] = {
#         "abx": {
#                 "id": "abx",
#                 "name": "Table",
#                 "price": 5980,
#                 "store_id": "1",
#                 "store": {
#                     "id": "1",
#                     "name": "Funiture Store",
#                 },
#             },

#         "axb2": {
#                 "id": "axb2",
#                 "name": "Chair",
#                 "price": 6500,
#                 "store_id": "1",
#                 "store": {
#                     "id": "1",
#                     "name": "Funiture Store",
#                 },
#             }
#     }

#     stores:dict[str, dict] = {
#         "1":{
#             "id": "1",
#             "name": "Funiture Store",
#             "items": [
#                 {
#                     "id": "abx",
#                     "name": "Table",
#                     "price": 5980,
#                 },

#                 {
#                     "id": "axb2",
#                     "name": "Chair",
#                     "price": 6500,
#                 },
#             ]
#         }
#     }
    
