from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from colossus.apps.accounts.forms import UserForm

from .models import User


class ProfileView(LoginRequiredMixin, UpdateView):
    """
    This is the class for displaying the user profile.
    """
    model = User
    form_class = UserForm
    template_name = 'accounts/profile.html'
    success_url = reverse_lazy('profile')

    def get_object(self, queryset=None):
        """
        This getter function gets the user object.
        """
        return self.request.user
