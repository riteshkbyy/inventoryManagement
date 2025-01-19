from django.urls import path
from .views import supplier_list, supplier_create, supplier_update, supplier_delete

urlpatterns = [
    path("", supplier_list, name="supplier_list"),
    path("suppliers/add/", supplier_create, name="supplier_create"),
    path("suppliers/edit/<str:id>/", supplier_update, name="supplier_update"),
    path("suppliers/delete/<str:id>/", supplier_delete, name="supplier_delete"),
]
