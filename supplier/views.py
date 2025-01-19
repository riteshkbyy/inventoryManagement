from django.shortcuts import render, redirect
from django.http import JsonResponse
from bson.objectid import ObjectId
from .forms import SupplierForm
from django.conf import settings

# Get MongoDB Collection
SUPPLIERS_COLLECTION  = settings.MONGO_DB["suppliers"] 


# List all suppliers
def supplier_list(request):
    suppliers = list(SUPPLIERS_COLLECTION.find({}))
    for supplier in suppliers:
        supplier["id"] = str(supplier["_id"])  # Convert ObjectId to string
    return render(request, "supplier/supplier_list.html", {"suppliers": suppliers})


# Create a new supplier
def supplier_create(request):
    if request.method == "POST":
        form = SupplierForm(request.POST)
        if form.is_valid():
            supplier_data = form.cleaned_data
            SUPPLIERS_COLLECTION.insert_one(supplier_data)
            return redirect("supplier_list")
    else:
        form = SupplierForm()
    return render(request, "supplier/supplier_form.html", {"form": form})


# Update an existing supplier
def supplier_update(request, id):
    supplier = SUPPLIERS_COLLECTION.find_one({"_id": ObjectId(id)})
    if not supplier:
        return JsonResponse({"error": "Supplier not found"}, status=404)

    if request.method == "POST":
        form = SupplierForm(request.POST)
        if form.is_valid():
            updated_data = form.cleaned_data
            SUPPLIERS_COLLECTION.update_one({"_id": ObjectId(id)}, {"$set": updated_data})
            return redirect("supplier_list")
    else:
        form = SupplierForm(initial=supplier)
    return render(request, "supplier/supplier_form.html", {"form": form})


# Delete a supplier
def supplier_delete(request, id):
    supplier = SUPPLIERS_COLLECTION.find_one({"_id": ObjectId(id)})
    if not supplier:
        return JsonResponse({"error": "Supplier not found"}, status=404)

    if request.method == "POST":
        SUPPLIERS_COLLECTION.delete_one({"_id": ObjectId(id)})
        return redirect("supplier_list")
    return render(request, "supplier/supplier_confirm_delete.html", {"supplier": supplier})
