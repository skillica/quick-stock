import uuid

# from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from core.mixins import OwnerQuerySetMixin

from .forms import ProductForm
from .models import Product


# PascalCase , snake_case
class ProductListView(OwnerQuerySetMixin, ListView):
    model = Product
    template_name = "inventory/product_list.html"
    context_object_name = "products"
    ordering = "name"

    def get_queryset(self):
        qs = super().get_queryset()
        search = self.request.GET.get("search")
        sort = self.request.GET.get("sort")  # oldest

        if search:
            qs = qs.filter(Q(name__icontains=search) | Q(sku__icontains=search))

        SORT_MAP = {
            "name_asc": "name",
            "name_desc": "-name",
            "price_asc": "price",
            "price_desc": "-price",
            "newest": "-created_at",
            "oldest": "created_at",
        }

        if sort in SORT_MAP:
            qs = qs.order_by(SORT_MAP[sort])

        return qs


class ProductDetailView(OwnerQuerySetMixin, DetailView):
    model = Product
    template_name = "inventory/product_detail.html"


class ProductCreateView(OwnerQuerySetMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = "inventory/product_form.html"
    success_url = reverse_lazy("inventory:list")

    def form_valid(self, form):
        form.instance.sku = f"{uuid.uuid4()}"[:8]
        form.instance.user = self.request.user
        return super().form_valid(form)


class ProductUpdateView(OwnerQuerySetMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "inventory/product_form.html"
    success_url = reverse_lazy("inventory:list")
    context_object_name = "product"  # object.


class ProductDeleteView(OwnerQuerySetMixin, DeleteView):
    model = Product
    template_name = "inventory/product_delete.html"
    success_url = reverse_lazy("inventory:list")


# def product_list_view(request):
#     products = Product.objects.all()
#     return render(request, "product_list.html", {"products": products})


# Create your views here.
# CBV vs FBV
# summary
# report graph
# report graph 2
# invoice -> main task -> email # invoice db save -> email, logging
# models -> managers -> signal -> forms -> views -> urls -> templates
# def product_list_view(request):

# flask, fastapi
