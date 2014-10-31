from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation import ugettext as _
from forms import SignupForm, LoginForm, CustomerForm, AgentForm, SysAdminForm
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from models import BaseUser, SysAdmin, Agent, Customer
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.contrib.messages import info, error
from django.http import Http404
from django import forms
from django.conf import settings
from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url
from django.http import HttpResponse


class CompanyList(ListView):
    model = SysAdmin
    template_name = 'company_list.html'
    context_object_name = 'admins'


def refresh_captcha(request):
    if request.GET.get('newsn') == '1':
        csn = CaptchaStore.generate_key()
        cimageurl = captcha_image_url(csn)
        return HttpResponse(cimageurl)


# Create your views here.
def login(request, template="accounts/account_login.html"):
    """
    Login form.
    """
    print '*'*20
    form = LoginForm(request.POST or None)
    msg = ''
    #print form.is_valid()
    if request.method == "POST":
        if form.is_valid():
            try:
                authenticated_user = form.save()
                if authenticated_user is not None:
                    if authenticated_user.is_active:
                        auth_login(request, authenticated_user)
                    # Redirect to a success page.
                    #TODO redirect to core.dashboard page
                    return redirect('core.dashboard')
            except forms.ValidationError as e:
                print e
                msg = e
        else:
            msg = _('Invalid Captcha')

    print '%'*20
    context = {"form": form, "title": _("Log in"), 'msg': msg}
    return render(request, template, context)


def signup(request, template="accounts/account_signup.html"):
    """
    Signup form.
    """

    form = SignupForm(request.POST or None)
    msg = ''
    if request.method == 'POST':
        print form.is_valid()
        if form.is_valid():
            try:
                new_user = form.save()
                info(request, _("Successfully signed up"))
                auth_login(request, new_user)
                return redirect('core.dashboard')
            except forms.ValidationError as e:
                error(request, e.message)
                msg = e
                print e
        else:
            msg = _('Invalid Captcha')

    context = {"form": form, "title": _("Sign up"), 'msg': msg}
    return render(request, template, context)


def password_reset(request):
    msg = ''
    if request.method == 'POST':
        username_or_password = request.POST.get('username')
        print username_or_password
        from django.db.models import Q
        user = None
        try:
            user = User.objects.get(Q(username=username_or_password) | Q(email=username_or_password))
        except User.DoesNotExist:
            msg = _('User does not exist')
            error(request, msg)
        if user:
            #send Email to user
            from django.core import mail
            #TODO
            password_reset_link = 'reset_url'
            print user.email
            result = mail.send_mail(_('Password Reset Mail'), password_reset_link, settings.EMAIL_HOST_USER, [user.email])
            if result == 1:
                msg = _('Check your Email for password reset link')

    return render(request, 'accounts/account_password_reset.html', {'msg': msg})


def logout(request):
    auth_logout(request)
    return redirect('login')


def profile(request, template='accounts/account_profile.html'):
    #print BaseUser.objects.all()
    #print request.user.pk
    #print request.user.username
    u = User.objects.get(id=request.user.pk)
    print u.groups.all()
    #base_user = get_object_or_404(BaseUser, user_id=request.user.pk)
    #print base_user
    print request.user.pk
    print request.user.username
    print request.user.groups.all()
    groups = request.user.groups.values_list('name', flat=True)
    print groups

    def update_user(user, form):
            for k, v in form.cleaned_data.items():
                print k, v
                setattr(user, k, v)
            #agent.password = form.cleaned_data.get('password')
            #agent.phone = form.cleaned_data.get("phone")
            user.save()

            u.email = user.email
            from django.contrib.auth.hashers import (
            check_password, make_password, is_password_usable)
            u.password = make_password(user.password)
            u.save()
    if 'AgentGroup' in groups:
        agent = get_object_or_404(Agent, username=request.user.username)
        #form = AgentForm(request.POST or None, initial={'username': agent.username, 'phone': agent.phone})
        form = AgentForm(request.POST or None, instance=agent)
        if request.method == "POST" and form.is_valid():
            update_user(agent, form)
            info(request, _("Agent updated"))
        context = {"form": form, "title": _("Update Agent")}
        return render(request, template, context)
    elif 'CustomerGroup' in groups:
        customer = get_object_or_404(Customer, username=request.user.username)
        form = CustomerForm(request.POST or None, instance=customer)
        if request.method == "POST" and form.is_valid():
            update_user(customer, form)
            info(request, _("Customer updated"))
        context = {"form": form, "title": _("Update Customer")}
        return render(request, template, context)
    elif 'SuperAdminGroup' in groups or 'AdminGroup' in groups:
        admin = get_object_or_404(SysAdmin, username=request.user.username)
        form = SysAdminForm(request.POST or None, instance=admin)
        if request.method == "POST" and form.is_valid():
            update_user(admin, form)
            #TODO change group if necessary
            info(request, _("SysAdmin updated"))
        context = {"form": form, "title": _("Update SysAdmin")}
        return render(request, template, context)

    return render(request, template)


class SysAdminList(ListView):
    model = SysAdmin
    template_name = 'sysadmin_list.html'
    context_object_name = 'sysadmins'


class SysAdminCreate(CreateView):
    model = SysAdmin
    form_class = SysAdminForm
    template_name = 'create_project.html'

    success_url = reverse_lazy('accounts.sysadmins')

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(SysAdminCreate, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['title'] = _('Create')
        context['model_name'] = _('System Admin')
        return context


class SysAdminUpdate(UpdateView):
    model = SysAdmin
    form_class = SysAdminForm
    template_name = 'create_project.html'
    success_url = reverse_lazy('accounts.sysadmins')

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(SysAdminUpdate, self).get_context_data(**kwargs)
        # Add extra context variable
        context['title'] = _('Modify SysAdmin')
        return context


class SysAdminDelete(DeleteView):
    model = SysAdmin
    template_name = 'gateway_confirm_delete.html'
    success_url = reverse_lazy('accounts.sysadmins')


class AgentList(ListView):
    model = Agent
    template_name = 'agent_list.html'
    context_object_name = 'agents'


class AgentCreate(CreateView):
    model = Agent
    form_class = AgentForm
    template_name = 'create_project.html'

    success_url = reverse_lazy('accounts.agents')

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(AgentCreate, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['title'] = _('Create')
        context['model_name'] = _('Agents')
        return context


class AgentUpdate(UpdateView):
    model = Agent
    form_class = AgentForm
    template_name = 'create_project.html'
    success_url = reverse_lazy('accounts.agents')

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(AgentUpdate, self).get_context_data(**kwargs)
        # Add extra context variable
        context['title'] = _('Modify Agent')
        return context


class AgentDelete(DeleteView):
    model = Agent
    template_name = 'gateway_confirm_delete.html'
    success_url = reverse_lazy('accounts.agents')


class CustomerList(ListView):
    model = Customer
    template_name = 'customer_list.html'
    context_object_name = 'customers'


class CustomerCreate(CreateView):
    model = Customer
    form_class = CustomerForm
    template_name = 'create_project.html'

    success_url = reverse_lazy('accounts.customers')

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(CustomerCreate, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['title'] = _('Create')
        context['model_name'] = _('Customers')
        return context


class CustomerUpdate(UpdateView):
    model = Customer
    form_class = CustomerForm
    template_name = 'create_project.html'
    success_url = reverse_lazy('accounts.customers')

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(CustomerUpdate, self).get_context_data(**kwargs)
        # Add extra context variable
        context['title'] = _('Modify Customer')
        return context


class CustomerDelete(DeleteView):
    model = Customer
    template_name = 'gateway_confirm_delete.html'
    success_url = reverse_lazy('accounts.customers')



