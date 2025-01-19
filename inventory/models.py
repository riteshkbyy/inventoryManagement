from django.conf import settings
from bson.objectid import ObjectId
from stock_movement.models import StockMovement  # Import StockMovement


class Product:
    collection = settings.MONGO_DB["products"]

    @staticmethod
    def create(name, description, price, stock, supplier_id):
        data = {
            "name": name,
            "description": description,
            "price": price,
            "stock": stock,
            "supplier_id": ObjectId(supplier_id)
        }
        
        return Product.collection.insert_one(data)

    @staticmethod
    def get_all():
        return list(Product.collection.find())

    @staticmethod
    def get_by_id(product_id):
        return Product.collection.find_one({"_id": ObjectId(product_id)})

    @staticmethod
    def update(product_id, update_data):
        print("uuu")
        StockMovement.create_stock_movement(
            update_data["product_id"], update_data["quantity"], "IN", order_id = None
        )
        return Product.collection.update_one({"_id": ObjectId(product_id)}, {"$set": update_data})

    @staticmethod
    def delete(product_id):
        return Product.collection.delete_one({"_id": ObjectId(product_id)})
    
    @property
    def id(self):
        return str(self._id)
    

