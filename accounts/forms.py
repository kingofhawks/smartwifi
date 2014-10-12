from __future__ import unicode_literals
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.db.models import Q
from django.db.models.manager import Manager
from django import forms
from django.utils.http import int_to_base36
from django.utils.translation import ugettext, ugettext_lazy as _
from django.forms import ModelForm
from models import Customer, Agent, SysAdmin
from django.shortcuts import get_object_or_404
from django.http import Http404


class SignupForm(forms.Form):
    username = forms.CharField(label=_("Username"))
    email = forms.EmailField(label=_("Email"))
    password1 = forms.CharField(widget=forms.PasswordInput(render_value=False),
                                label=_("Create password"))
    password2 = forms.CharField(widget=forms.PasswordInput(render_value=False),
                                label=_("Repeat password"))

    def save(self, *args, **kwargs):
        """
        Create the new user. If no username is supplied (may be hidden
        via ``ACCOUNTS_PROFILE_FORM_EXCLUDE_FIELDS`` or
        ``ACCOUNTS_NO_USERNAME``), we generate a unique username, so
        that if profile pages are enabled, we still have something to
        use as the profile's slug.
        """
        username, email, password1, password2 = (self.cleaned_data['username'],
                                     self.cleaned_data['email'],
                                     self.cleaned_data['password1'],
                                     self.cleaned_data['password2'])
        if password1 != password2:
            raise forms.ValidationError(_("Password not match"))

        try:
            existing_user = get_object_or_404(User, username=username)
            if existing_user:
                raise forms.ValidationError(_("Username already exists"))
        except Http404:
            pass

        new_user = User.objects.create_user(username, email, password1)
        user = authenticate(username=username, password=password1)
        return user


class LoginForm( forms.Form):
    """
    Fields for login.
    """
    username = forms.CharField(label=_("Username"))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput(render_value=False))

    def save(self):
        """
        Just return the authenticated user - used for logging in.
        """
        """
        Authenticate the given username/email and password. If the fields
        are valid, store the authenticated user for returning via save().
        """
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        user = authenticate(username=username, password=password)
        if user is None:
            raise forms.ValidationError(_("Invalid username/email and password"))
        elif not user.is_active:
            raise forms.ValidationError(ugettext("Your account is inactive"))
        return user


class PasswordResetForm(forms.Form):
    """
    Validates the user's username or email for sending a login
    token for authenticating to change their password.
    """

    username = forms.CharField(label=_("Username"))

    def clean(self):
        username = self.cleaned_data.get("username")
        username_or_email = Q(username=username) | Q(email=username)
        try:
            user = User.objects.get(username_or_email, is_active=True)
        except User.DoesNotExist:
            raise forms.ValidationError(
                             ugettext("Invalid username/email"))
        else:
            self._user = user
        return self.cleaned_data

    def save(self):
        """
        Just return the authenticated user - used for sending login
        email.
        """
        return getattr(self, "_user", None)


class UserForm(ModelForm):
    class Meta:
        model = User
        #include = ['username']
        exclude = ['date_joined', 'is_superuser', 'is_staff', 'last_login', 'is_super_user', 'user_permissions']


class SysAdminForm(ModelForm):
    class Meta:
        model = SysAdmin
        exclude = ['user']
        widgets = {
            'password': forms.PasswordInput(),
        }


class AgentForm(ModelForm):
    class Meta:
        model = Agent
        exclude = ['user']
        widgets = {
            'password': forms.PasswordInput(),
        }


class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        exclude = ['user']
        widgets = {
            'password': forms.PasswordInput(),
        }




