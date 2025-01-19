# models.py (StockMovement App)
from django.conf import settings
from datetime import datetime

# MongoDB connection

stock_movement_collection = settings.MONGO_DB["stock_movement"]

class StockMovement:
    MOVEMENT_TYPES = ['IN', 'OUT']
    
    @staticmethod
    def create_stock_movement(product_id, quantity, movement_type, order_id=None):
        # Create a new stock movement
        stock_movement = {
            "product_id": product_id,
            "quantity": quantity,
            "movement_type": movement_type,
            "order_id": order_id,
            "timestamp": datetime.utcnow()
        }
        stock_movement_collection.insert_one(stock_movement)
    
    @staticmethod
    def get_all_movements():
        # Fetch all stock movements from the collection
        return list(stock_movement_collection.find())

    @staticmethod
    def get_movement_by_id(movement_id):
        # Fetch a stock movement by its ID
        return stock_movement_collection.find_one({"_id": movement_id})

    @staticmethod
    def update_stock_movement(movement_id, data):
        # Update stock movement (e.g., quantity)
        stock_movement_collection.update_one({"_id": movement_id}, {"$set": data})
