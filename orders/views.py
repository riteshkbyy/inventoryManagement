from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import SalesOrder
from bson import ObjectId
from django.conf import settings

orders_collection = settings.MONGO_DB["orders"]

products_collection = settings.MONGO_DB["products"]
def order_list(request):
    orders = list(orders_collection.find())
    for order in orders:
        order["id"] = str(order["_id"])
        order["product_id"] = str(order["product_id"])
    return render(request, "orders/order_list.html", {"orders": orders})

def create_order(request):
    if request.method == "POST":
        customer_name = request.POST["customer_name"]
        product_id = request.POST["product_id"]
        quantity = int(request.POST["quantity"])
        try:
            order_id = SalesOrder.create_order(customer_name, product_id, quantity)
            return redirect("orders:order_list")
        except ValueError as e:
            return render(request, "orders/create_order.html", {"error_message": str(e)})

    products = list(products_collection.find())
    for product in products:
        product["id"] = str(product["_id"])

    return render(request, "orders/create_order.html", {"products": products})

def complete_order(request, order_id):
    try:
        SalesOrder.complete_order(order_id)
    except ValueError as e:
        return JsonResponse({"error": str(e)}, status=400)
    return redirect("orders:order_list")

def cancel_order(request, order_id):
    try:
        SalesOrder.cancel_order(order_id)
    except ValueError as e:
        return JsonResponse({"error": str(e)}, status=400)
    return redirect("orders:order_list")
