from django.shortcuts import render
from django.conf import settings


products_collection = settings.MONGO_DB["products"]
def stock_list(request):
    """ Fetch product stock details from MongoDB """
    products = list(products_collection.find({}, {"_id": 1, "name": 1, "stock": 1}))
    for product in products:
        product["id"] = str(product["_id"])  # Convert ObjectId to string

    return render(request, "stock_movement/stock_list.html", {"products": products})
        

    