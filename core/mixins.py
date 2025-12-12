from django.contrib.auth.mixins import LoginRequiredMixin


class OwnerQuerySetMixin(LoginRequiredMixin):
    owner_field = "user"

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(**{self.owner_field: self.request.user})
        return qs
