from __future__ import unicode_literals
from django.contrib.auth import authenticate
from django.contrib.auth.models import User, Group
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
from captcha.fields import CaptchaField

TYPE_CHOICES = (('1', _('Agent'),), ('2', _('Second'),))


class SignupForm(forms.Form):
    username = forms.CharField(label=_("Username"))
    email = forms.EmailField(label=_("Email"))
    password1 = forms.CharField(widget=forms.PasswordInput(render_value=False),
                                label=_("Create password"))
    password2 = forms.CharField(widget=forms.PasswordInput(render_value=False),
                                label=_("Repeat password"))
    type = forms.ChoiceField(widget=forms.RadioSelect, choices=TYPE_CHOICES)
    captcha = CaptchaField()

    def save(self, *args, **kwargs):
        """
        Create the new user. If no username is supplied (may be hidden
        via ``ACCOUNTS_PROFILE_FORM_EXCLUDE_FIELDS`` or
        ``ACCOUNTS_NO_USERNAME``), we generate a unique username, so
        that if profile pages are enabled, we still have something to
        use as the profile's slug.
        """
        account_type = self.cleaned_data['type']
        username, email, password1, password2 = (self.cleaned_data['username'],
                                     self.cleaned_data['email'],
                                     self.cleaned_data['password1'],
                                     self.cleaned_data['password2'])
        print 'user type:{} name:{} email:{}'.format(account_type, username, email)

        if password1 != password2:
            raise forms.ValidationError(_("Password not match"))

        try:
            existing_user = get_object_or_404(User, username=username)
            print '1'*20
            if existing_user:
                raise forms.ValidationError(_("Username already exists"))
        except Http404 as e:
            print e

        try:
            print '2'*20
            existing_user = get_object_or_404(User, email=email)
            print 'existing_user:{} email:{}'.format(existing_user, email)
            if existing_user:
                raise forms.ValidationError(_("Email already exists"))
        except Http404 as e:
            print e

        new_user = User.objects.create_user(username, email, password1)
        user = authenticate(username=username, password=password1)

        if int(account_type) == 1:
            agent_group = Group.objects.get(name='AgentGroup')
            print agent_group
            new_user.groups.add(agent_group)
            new_user.save()

            agent = Agent(user=new_user, username=username, email=email, password=password1, signup_flag=False)
            agent.save()
        elif int(account_type) == 2:
            customer_group = Group.objects.get(name='CustomerGroup')
            print customer_group
            new_user.groups.add(customer_group)
            new_user.save()

            customer = Customer(user=new_user, username=username, email=email, password=password1, signup_flag=False)
            customer.save()
        else:
            print 'incorrect account_type:{}'.format(account_type)
        return user


class LoginForm(forms.Form):
    """
    Fields for login.
    """
    username = forms.CharField(label=_("Username"))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput(render_value=False))
    captcha = CaptchaField()


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




