from pymongo import MongoClient
from bson import ObjectId
from django.conf import settings
from stock_movement.models import StockMovement  # Import StockMovement

# Connect to MongoDB

orders_collection = settings.MONGO_DB["orders"]

products_collection = settings.MONGO_DB["products"]

class SalesOrder:
    STATUS_PENDING = "pending"
    STATUS_COMPLETED = "completed"
    STATUS_CANCELED = "canceled"
    VALID_STATUSES = [STATUS_PENDING, STATUS_COMPLETED, STATUS_CANCELED]

    @staticmethod
    def create_order(customer_name, product_id, quantity):
        product = products_collection.find_one({"_id": ObjectId(product_id)})
        if not product:
            raise ValueError("Product not found.")

        if product["stock"] < quantity:
            raise ValueError("Insufficient stock.")

        order_data = {
            "customer_name": customer_name,
            "product_id": ObjectId(product_id),
            "quantity": quantity,
            "status": SalesOrder.STATUS_PENDING
        }
        order_id = orders_collection.insert_one(order_data).inserted_id

        # Reduce stock level
        products_collection.update_one(
            {"_id": ObjectId(product_id)},
            {"$inc": {"stock": -quantity}}
        )
        StockMovement.create_stock_movement(
            product_id, quantity, "OUT", order_id
        )
        return str(order_id)

    @staticmethod
    def complete_order(order_id):
        order = orders_collection.find_one({"_id": ObjectId(order_id)})
        if not order:
            raise ValueError("Order not found.")
        if order["status"] != SalesOrder.STATUS_PENDING:
            raise ValueError("Only pending orders can be completed.")

        orders_collection.update_one(
            {"_id": ObjectId(order_id)},
            {"$set": {"status": SalesOrder.STATUS_COMPLETED}}
        )

    @staticmethod
    def cancel_order(order_id):
        order = orders_collection.find_one({"_id": ObjectId(order_id)})
        if not order:
            raise ValueError("Order not found.")
        if order["status"] != SalesOrder.STATUS_PENDING:
            raise ValueError("Only pending orders can be canceled.")

        # Restock the product
        products_collection.update_one(
            {"_id": ObjectId(order["product_id"])},
            {"$inc": {"stock": order["quantity"]}}
        )

        orders_collection.update_one(
            {"_id": ObjectId(order_id)},
            {"$set": {"status": SalesOrder.STATUS_CANCELED}}
        )
        StockMovement.create_stock_movement(
            order["product_id"], order["quantity"], "IN", order_id
        )
        return True
