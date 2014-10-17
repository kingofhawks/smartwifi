from django.db import models
from django.contrib.auth.models import User, Group
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver


class BaseUser(models.Model):
    user = models.OneToOneField(User, blank=True, null=True)
    username = models.CharField(verbose_name=_('Username'), max_length=32)
    password = models.CharField(verbose_name=_('Password'), max_length=32)
    #full_name = models.CharField(verbose_name=_('Full Name'), max_length=32, blank=True, null=True)
    phone = models.CharField(verbose_name=_('Phone'), max_length=32, blank=True, null=True)
    qq = models.CharField(verbose_name=_('QQ'), max_length=32, blank=True, null=True)
    email = models.EmailField(verbose_name=_('Email'), max_length=32, blank=True, null=True)
    override_ad1 = models.BooleanField(verbose_name=_('override_ad1'), default=False)
    ad1 = models.ForeignKey('management.Ad', verbose_name=_('ad1'), related_name='ad1', blank=True, null=True)
    override_ad2 = models.BooleanField(verbose_name=_('override_ad2'), default=False)
    ad2 = models.ForeignKey('management.Ad', verbose_name=_('ad2'), related_name='ad2', blank=True, null=True)
    override_ad3 = models.BooleanField(verbose_name=_('override_ad3'), default=False)
    ad3 = models.ForeignKey('management.Ad', verbose_name=_('ad3'), related_name='ad3', blank=True, null=True)
    override_ssid = models.BooleanField(verbose_name=_('override_ssid'), default=False)
    ssid = models.CharField(verbose_name=_('SSID'), max_length=64, blank=True, null=True)
    sms_template = models.CharField(verbose_name=_('SMS Template'), max_length=256, blank=True, null=True)
    comment = models.CharField(verbose_name=_('Comment'), max_length=512, blank=True, null=True)
    signup_flag = models.BooleanField(default=True)

    def __unicode__(self):
        return self.username


class SysAdmin(BaseUser):
    super_admin = models.BooleanField(verbose_name=_('Super Admin'), default=True)


class Agent(BaseUser):
    full_name = models.CharField(verbose_name=_('Full Name'), max_length=32, blank=True, null=True)


class Customer(BaseUser):
    full_name = models.CharField(verbose_name=_('Full Name'), max_length=32, blank=True, null=True)
    agent = models.ForeignKey(Agent, verbose_name=_('Agent'), blank=True, null=True)


# method for create user after create Agent
@receiver(post_save, sender=Agent)
def create_agent_user(sender, instance, **kwargs):
    print sender
    print '**' * 10
    print kwargs
    print instance
    print instance.username
    print instance.password
    if kwargs['created'] and instance.signup_flag:
        new_user = User.objects.create_user(instance.username, instance.email, instance.password)

        #add user to AgentGroup
        agent_group = Group.objects.get(name='AgentGroup')
        print agent_group
        new_user.groups.add(agent_group)
        new_user.save()

        agent = Agent.objects.get(username= instance.username)
        agent.user = new_user
        agent.save()


@receiver(post_save, sender=SysAdmin)
def create_admin_user(sender, instance, **kwargs):
    print sender
    print '**' * 10
    print kwargs
    print instance
    print instance.username
    print instance.password
    if kwargs['created']:
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


@receiver(post_save, sender=Customer)
def create_customer_user(sender, instance, **kwargs):
    print sender
    print '**' * 10
    print kwargs
    print instance
    print instance.username
    print instance.password
    if kwargs['created'] and instance.signup_flag:
        new_user = User.objects.create_user(instance.username, instance.email, instance.password)

        #add user to AgentGroup
        customer_group = Group.objects.get(name='CustomerGroup')
        print customer_group
        new_user.groups.add(customer_group)
        new_user.save()

        customer = Customer.objects.get(username=instance.username)
        customer.user = new_user
        customer.save()

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




