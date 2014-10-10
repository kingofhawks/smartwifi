from django.db import models
from django.contrib.auth.models import User, Group
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser,UserManager, PermissionsMixin,AbstractUser)
from django.core import validators
from django.utils import timezone
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver


# Create your models here.
#class UserProfile(AbstractBaseUser, PermissionsMixin):
#    email = models.EmailField(verbose_name= 'email address', max_length=255, unique=True)
#    username = models.CharField(_('username'), max_length=30, unique=True,
#        help_text=_('Required. 30 characters or fewer. Letters, digits and '
#                    '@/./+/-/_ only.'),
#        validators=[
#            validators.RegexValidator(r'^[\w.@+-]+$', _('Enter a valid username.'), 'invalid')
#        ])
#    company = models.CharField(_('company'), max_length= 255, blank=False)
#    is_active = models.BooleanField(default=True)
#    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
#
#    objects = UserManager()
#    USERNAME_FIELD = 'username'
#    REQUIRED_FIELDS = ['company','email']
#
#    # On Python 3: def __str__(self):
#    def __unicode__(self):
#        return self.username
#
#    def get_full_name(self):
#        return self.company
#
#    def get_short_name(self):
#        "Returns the short name for the user."
#        return self.username
#
#    def has_perm(self, perm, obj=None):
#        return True
#
#    def has_module_perms(self, app_label):
#        return True


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    company = models.CharField(verbose_name=_('Company'), max_length=255, blank=False)
    location = models.CharField(verbose_name=_("location"), max_length=256, blank=True, null=True)
    contact = models.CharField(verbose_name=_('contact'), max_length=32, blank=True, null=True)
    phone = models.CharField(verbose_name=_('phone'), max_length=32, blank=True, null=True)

    def __str__(self):
        return self.company


class BaseUser(models.Model):
    user = models.OneToOneField(User, blank=True, null=True)
    username = models.CharField(verbose_name=_('Username'), max_length=32)
    password = models.CharField(verbose_name=_('Password'), max_length=32)
    #full_name = models.CharField(verbose_name=_('Full Name'), max_length=32, blank=True, null=True)
    phone = models.CharField(verbose_name=_('Phone'), max_length=32, blank=True, null=True)
    qq = models.CharField(verbose_name=_('QQ'), max_length=32, blank=True, null=True)
    email = models.EmailField(verbose_name=_('Email'), max_length=32, blank=True, null=True)
    override_ad1 = models.BooleanField(verbose_name=_('override_ad1'), default=False)
    ad1 = models.CharField(verbose_name=_('ad1'), max_length=128, blank=True, null=True)
    override_ad2 = models.BooleanField(verbose_name=_('override_ad2'), default=False)
    ad2 = models.CharField(verbose_name=_('ad2'), max_length=128, blank=True, null=True)
    override_ad3 = models.BooleanField(verbose_name=_('override_ad3'), default=False)
    ad3 = models.CharField(verbose_name=_('ad3'), max_length=128, blank=True, null=True)
    override_ssid = models.BooleanField(verbose_name=_('override_ssid'), default=False)
    ssid = models.CharField(verbose_name=_('SSID'), max_length=64, blank=True, null=True)
    sms_template = models.CharField(verbose_name=_('SMS Template'), max_length=256, blank=True, null=True)
    comment = models.CharField(verbose_name=_('Comment'), max_length=512, blank=True, null=True)
    #agent = models.ForeignKey('self')

    def __unicode__(self):
        return self.username


class SysAdmin(BaseUser):
    super_admin = models.BooleanField(verbose_name=_('Super Admin'), default=True)


class Agent(BaseUser):
    full_name = models.CharField(verbose_name=_('Full Name'), max_length=32, blank=True, null=True)


class Customer(BaseUser):
    full_name = models.CharField(verbose_name=_('Full Name'), max_length=32, blank=True, null=True)
    agent = models.ForeignKey(Agent)


# method for create user after create Agent
@receiver(post_save, sender=Agent)
def create_agent_user(sender, instance, **kwargs):
    print sender
    print '**' * 10
    print kwargs
    print instance
    print instance.username
    print instance.password
    # user = User.objects.get(username=instance)
    # print user
    # print user.groups.all()
    # #user.password = '11111'
    # #user.save()
    # print 'count:{}'.format(user.groups.filter(name='AgentGroup').count())
    # groups = user.groups.values_list('name',flat=True)
    # print user.groups.all()
    # print groups
    if kwargs['created']:
        #Update the not hashed user password
        # from django.contrib.auth.hashers import make_password
        # user.password = make_password(user.password)
        new_user = User.objects.create_user(instance.username, instance.email, instance.password)

        #add user to AgentGroup
        agent_group = Group.objects.get(name='AgentGroup')
        print agent_group
        new_user.groups.add(agent_group)
        new_user.save()

        agent = Agent.objects.get(username= instance.username)
        agent.user = new_user
        agent.save()
        # user.save()
        # agent = BaseUser(user=user)
        # agent.save()


@receiver(post_save, sender=SysAdmin)
def create_admin_user(sender, instance, **kwargs):
    print sender
    print '**' * 10
    print kwargs
    print instance
    print instance.username
    print instance.password
    # user = User.objects.get(username=instance)
    # print user
    # print user.groups.all()
    # #user.password = '11111'
    # #user.save()
    # print 'count:{}'.format(user.groups.filter(name='AgentGroup').count())
    # groups = user.groups.values_list('name',flat=True)
    # print user.groups.all()
    # print groups
    if kwargs['created']:
        #Update the not hashed user password
        # from django.contrib.auth.hashers import make_password
        # user.password = make_password(user.password)
        new_user = User.objects.create_user(instance.username, instance.email, instance.password)

        #add user to AgentGroup
        if instance.super_admin:
            super_admin_group = Group.objects.get(name='SuperAdminGroup')
            new_user.groups.add(super_admin_group)
            new_user.save()
        else:
            admin_group = Group.objects.get(name='AdminGroup')
            new_user.groups.add(admin_group)
            new_user.save()

        sys_admin = SysAdmin.objects.get(username=instance.username)
        sys_admin.user = new_user
        sys_admin.save()
        # user.save()
        # agent = BaseUser(user=user)
        # agent.save()


@receiver(post_save, sender=Customer)
def create_customer_user(sender, instance, **kwargs):
    print sender
    print '**' * 10
    print kwargs
    print instance
    print instance.username
    print instance.password
    # user = User.objects.get(username=instance)
    # print user
    # print user.groups.all()
    # #user.password = '11111'
    # #user.save()
    # print 'count:{}'.format(user.groups.filter(name='AgentGroup').count())
    # groups = user.groups.values_list('name',flat=True)
    # print user.groups.all()
    # print groups
    if kwargs['created']:
        #Update the not hashed user password
        # from django.contrib.auth.hashers import make_password
        # user.password = make_password(user.password)
        new_user = User.objects.create_user(instance.username, instance.email, instance.password)

        #add user to AgentGroup
        customer_group = Group.objects.get(name='CustomerGroup')
        print customer_group
        new_user.groups.add(customer_group)
        new_user.save()

        customer = Customer.objects.get(username=instance.username)
        customer.user = new_user
        customer.save()
        # user.save()
        # agent = BaseUser(user=user)
        # agent.save()

# @receiver(pre_save, sender=Agent)
# def create_profile(sender, instance, **kwargs):
#     print sender
#     print '**' * 10
#     print kwargs
#     print instance.user
#     print instance
#     print type(instance)


#@receiver(post_delete, sender=SysAdmin)
@receiver(post_delete)
def delete_admin_user(sender, instance, **kwargs):
    print sender
    list_of_models = ('SysAdmin', 'Agent', 'Customer')
    if sender.__name__ in list_of_models:
        print '**' * 10
        print kwargs
        print instance
        print instance.username
        user = User.objects.get(username=instance)
        print user
        user.delete()




