from django.db.models import Q
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, View

from core.mixins import LoginRequiredMixin, OwnerQuerySetMixin
from inventory.models import Product

from .models import Order, OrderItem


class OrderListView(OwnerQuerySetMixin, ListView):
    models = Order
    template_name = "orders/order_list.html"
    context_object_name = "orders"

    def get_queryset(self):
        return Order.objects.order_by("-created_at")


class OrderCreateView(CreateView):
    model = Order
    template_name = "orders/order_create.html"
    fields = ("customer_name", "status")
    success_url = reverse_lazy("orders:list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        order = form.save()
        items_ids = self.request.POST.getlist("item_id")
        Product.objects.select_for_update().get(id=4)

        for item_id in items_ids:
            product_id = self.request.POST.get(f"product_id_{item_id}")
            qty = self.request.POST.get(f"qty_{item_id}")
            price = self.request.POST.get(f"price_{item_id}")
            discount = self.request.POST.get(f"discount_{item_id}")

            if product_id and qty and price:
                OrderItem.objects.create(
                    order=order,
                    product_id=product_id,
                    qty=int(qty),
                    price=price,
                    discount=int(discount) if discount else 0,
                )

        items = order.items.all()
        sub_total = sum(item.price * item.qty for item in items)
        total_discount = sum(item.discount * item.qty for item in items)
        order.sub_total = sub_total
        order.total_discount = total_discount
        order.total_price = sub_total - total_discount
        order.save()
        return super().form_valid(form)


class ProductSearchView(LoginRequiredMixin, View):
    def get(self, request):
        query = request.GET.get("product-search", "").strip()

        if len(query) < 2:
            return HttpResponse("")

        products = Product.objects.filter(
            Q(name__icontains=query) | Q(sku__icontains=query)
        ).filter(user=request.user)

        html = render_to_string(
            "orders/partials/product_search_results.html",
            {"products": products, "query": query},
        )

        return HttpResponse(html)
