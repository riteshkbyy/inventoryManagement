from django.urls import path
from . import views

app_name = "orders"
urlpatterns = [
    path("", views.order_list, name="order_list"),
    path("create/", views.create_order, name="create_order"),
    path("complete/<str:order_id>/", views.complete_order, name="complete_order"),
    path("cancel/<str:order_id>/", views.cancel_order, name="cancel_order"),
]
