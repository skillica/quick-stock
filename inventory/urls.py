from django.urls import path

from .views import (
    ProductCreateView,
    ProductDeleteView,
    ProductDetailView,
    ProductListView,
    ProductUpdateView,
)

# from . import views

app_name = "inventory"

urlpatterns = [
    path("", ProductListView.as_view(), name="list"),
    path("create/", ProductCreateView.as_view(), name="create"),
    path("<int:pk>/detail", ProductDetailView.as_view(), name="detail"),
    path("<int:pk>/update", ProductUpdateView.as_view(), name="update"),
    path("<int:pk>/delete", ProductDeleteView.as_view(), name="delete"),
]
