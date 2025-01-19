from django.shortcuts import render, redirect
from django.http import JsonResponse
from pymongo import MongoClient
from bson import ObjectId
from stock_movement.models import StockMovement  # Import StockMovement

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["inventory_db"]
products_collection = db["products"]
suppliers_collection = db["suppliers"]

# ------------------------ PRODUCTS ------------------------

# List all products
def product_list(request):
    products = list(products_collection.find())
    
    for product in products:
        product["id"] = str(product["_id"])  # Convert ObjectId to string
        
        # Fetch supplier name
        if "supplier_id" in product and product["supplier_id"]:
            supplier = suppliers_collection.find_one({"_id": ObjectId(product["supplier_id"])})
            product["supplier_name"] = supplier["name"] if supplier else "Unknown Supplier"
        else:
            product["supplier_name"] = "No Supplier"

    return render(request, "inventory/product_list.html", {"products": products})

# Add a new product
def add_product(request):
    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description", "")
        price = float(request.POST.get("price", 0))
        stock = int(request.POST.get("stock", 0))
        supplier_id = request.POST.get("supplier_id")

        # Ensure supplier_id is a valid ObjectId
        supplier_id = ObjectId(supplier_id) if supplier_id else None

        result = products_collection.insert_one({
            "name": name,
            "description": description,
            "price": price,
            "stock": stock,
            "supplier_id": supplier_id
        })
        StockMovement.create_stock_movement(
            result.inserted_id, stock, "IN", order_id = None
        )
        return redirect("product_list")
    
    suppliers = list(suppliers_collection.find())
    for supplier in suppliers:
        supplier["id"] = str(supplier["_id"])
    
    return render(request, "inventory/add_product.html", {"suppliers": suppliers})

# Update a product
def update_product(request, product_id):
    product = products_collection.find_one({"_id": ObjectId(product_id)})
    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description", "")
        price = float(request.POST.get("price", 0))
        stock = int(request.POST.get("stock", 0))
        supplier_id = request.POST.get("supplier_id")

        # Ensure supplier_id is a valid ObjectId
        supplier_id = ObjectId(supplier_id) if supplier_id else None
        product_stock = products_collection.find_one({"_id": ObjectId(product_id)})["stock"]
        products_collection.update_one({"_id": ObjectId(product_id)}, {"$set": {
            "name": name,
            "description": description,
            "price": price,
            "stock": stock,
            "supplier_id": supplier_id
        }})
        if stock>product_stock:
            stock = stock - product_stock
            type = "IN"
            StockMovement.create_stock_movement(
            product_id, stock , type, order_id = None
        )
        elif stock<product_stock:
            stock = product_stock - stock
            type = "OUT"
            StockMovement.create_stock_movement(
            product_id, stock , type, order_id = None
        )
        

        return redirect("product_list")
    
    suppliers = list(suppliers_collection.find())
    for supplier in suppliers:
        supplier["id"] = str(supplier["_id"])

    return render(request, "inventory/update_product.html", {"product": product, "suppliers": suppliers})

# Delete a product
def delete_product(request, product_id):
    products_collection.delete_one({"_id": ObjectId(product_id)})
    return redirect("product_list")
