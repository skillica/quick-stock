from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import SignupForm


class UserSignupView(CreateView):
    template_name = "accounts/register.html"
    form_class = SignupForm
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)


class UserLoginView(LoginView):
    template_name = "accounts/login.html"
    redirect_authenticated_user = True
    next_page = "home"

    def form_valid(self, form):
        remember = self.request.POST.get("remember", None)

        if not remember:
            self.request.session.set_expiry(0)  # -1, 0, positive
        else:
            self.request.session.set_expiry(60 * 60 * 24 * 30)

        return super().form_valid(form)


class UserLogoutView(LogoutView):
    next_page = reverse_lazy("home")


# Session Based -> username, ip,
# Token Based -> id, email, expire_date, token_backlist -> token
