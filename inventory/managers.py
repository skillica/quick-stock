from django.db.models import F, Manager


class ProductManager(Manager):
    def in_stock(self):
        return self.filter(stock__gte=0)

    def low_stock(self):
        return self.filter(stock__lt=F("low_stock_threshold"))  # realtime
