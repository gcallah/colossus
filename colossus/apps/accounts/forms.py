from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _

import pytz

from .models import User


class AdminUserCreationForm(UserCreationForm):
    """
    This is a class used for admin sign-up forms.
    """
    class Meta:
        """
        The is the inner class to define form fields for admin sign-up forms.
        """
        model = User
        fields = ('username', 'email',)

    def save(self, commit=True):
        """
        The function to add a new admin user to the user database.

        Keyword arguments:
        commit -- A boolean variable to decide if the change must be commit or not.

        Returns:
        user -- The object of new user added into the database.
        """
        user = super().save(commit=False)
        user.is_staff = True
        user.is_superuser = True
        if commit:
            user.save()
        return user


class UserForm(forms.ModelForm):
    """
    This is a class used for user sign-up forms.
    """
    TIMEZONE_CHOICES = (('', '---------'),) + tuple(map(lambda tz: (tz, tz), pytz.common_timezones))

    timezone = forms.ChoiceField(
        choices=TIMEZONE_CHOICES,
        required=False,
        label=_('Timezone')
    )

    class Meta:
        """
        The is the inner class to define form fields for user (non-admins) sign-up forms.
        """
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password', 'timezone')
