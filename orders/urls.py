from django.urls import path

from .views import OrderCreateView, OrderListView, ProductSearchView

app_name = "orders"

urlpatterns = [
    path("", OrderListView.as_view(), name="list"),
    path("create/", OrderCreateView.as_view(), name="create"),
    path("product-search/", ProductSearchView.as_view(), name="product_search"),
]
