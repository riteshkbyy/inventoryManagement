# urls.py (StockMovement App)

from django.urls import path
from .views import stock_list

urlpatterns = [
    path('list/', stock_list, name='stock_list'),
]
