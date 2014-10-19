from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from datetime import datetime
from django.core.urlresolvers import reverse
from accounts.models import Customer, Agent
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import get_object_or_404


class Notification(models.Model):
    title = models.CharField(verbose_name=_('Title'), max_length=128)
    content = models.CharField(verbose_name=_('Content'), max_length=1024, default='', blank=True, null=True)
    creator = models.ForeignKey(User, verbose_name=_('Creator'), related_name='notification_creator')
    target = models.ForeignKey(User, verbose_name=_('Target'), blank=True, null=True, related_name='notification_target')
    processed = models.BooleanField(verbose_name=_('Processed'), default=False)
    date = models.DateTimeField(verbose_name=_('Date'), blank=True, null=True, default=datetime.utcnow())

    class Meta:
        verbose_name = _('Notification')
        permissions = (
            ("manage_notification", "Can manage notifications"),
        )

    def __unicode__(self):
        return u'Notification:{}'.format(self.content)


class Gateway(models.Model):
    gateway_name = models.CharField(verbose_name=_('Gateway Name'), max_length=128)
    mac = models.CharField(verbose_name=_('Mac'), max_length=128)
    customer = models.ForeignKey(Customer, verbose_name=_('Customer'))

    def __unicode__(self):
        return u'Gateway:{}'.format(self.gateway_name)


AD_TYPE_CHOICES = (
        (_('text_ad'), _('text_ad')),
        (_('img_ad'), _('img_ad')),
)


class Ad(models.Model):
    ad_type = models.CharField(verbose_name=_('Ad Type'), max_length=32, choices=AD_TYPE_CHOICES)
    ad_img = models.ImageField(verbose_name=_('AD Img'), upload_to="pictures", blank=True, null=True)
    ad_text = models.CharField(verbose_name=_('Ad Text'), max_length=128, blank=True, null=True)

    def __unicode__(self):
        return u'Ad:{}'.format(self.ad_text)


class AdStat(models.Model):
    ad = models.ForeignKey(Ad)
    showtime = models.DateTimeField(verbose_name=_('ShowTime'))
    count = models.IntegerField(verbose_name=_('Count'), default=1)

    def __unicode__(self):
        return u'AdStat:{}'.format(self.showtime)


class SmsTemplate(models.Model):
    name = models.CharField(verbose_name=_('Template Name'), max_length=64)
    template = models.CharField(verbose_name=_('SmsTemplate'), max_length=256)

    def __unicode__(self):
        return u'SmsTemplate:{}'.format(self.template)


class WifiClient(models.Model):
    gateway = models.ForeignKey(Gateway)
    username = models.CharField(verbose_name=_('Username'), max_length=256)
    phone = models.CharField(verbose_name=_('Phone'), max_length=11, blank=True, null=True, default='')
    mac = models.CharField(verbose_name=_('Mac'), max_length=128, blank=True, null=True)
    ip = models.CharField(verbose_name=_('IP'), max_length=64, blank=True, null=True)
    weixin = models.CharField(verbose_name=_('WeiXin'), max_length=128, blank=True, null=True)
    weibo = models.CharField(verbose_name=_('WeiBo'), max_length=128, blank=True, null=True)
    comment = models.CharField(verbose_name=_('Comment'), max_length=128, blank=True, null=True)
    last_login = models.DateTimeField(verbose_name=_('Last Login'), blank=True, null=True)
    cur_send_bytes = models.BigIntegerField(verbose_name=_('Current Send Bytes'), blank=True, null=True)
    cur_recv_bytes = models.BigIntegerField(verbose_name=_('Current Receive Bytes'), blank=True, null=True)
    total_send_bytes = models.BigIntegerField(verbose_name=_('Total Send Bytes'), blank=True, null=True)
    total_recv_bytes = models.BigIntegerField(verbose_name=_('Total Receive Bytes'), blank=True, null=True)
    token = models.CharField(verbose_name=_('Token'), max_length=128, blank=True, null=True)

    def __unicode__(self):
        return u'WifiClient:{}'.format(self.mac)


@receiver(signal=post_save, sender=Notification)
def create_notifications(sender, instance, **kwargs):
    if kwargs['created']:
        print '*'*20
        print instance.target
        print instance.creator
        print instance.creator.pk
        print instance.creator.groups.all()
        groups = instance.creator.groups.values_list('name', flat=True)
        if instance.target:
            return
        if 'AgentGroup' in groups:
            #Create notifications for all belonging customers
            agent = get_object_or_404(Agent, user=instance.creator)
            customers = Customer.objects.filter(agent=agent)
            print list(customers)
            for customer in customers:
                notification = Notification(title=instance.title,
                                            content=instance.content,
                                            creator=instance.creator, target=customer.user, date=instance.date)
                notification.save()
            pass
        elif 'SuperAdminGroup' in groups or 'AdminGroup' in groups:
            #Create notifications for all agents and customers
            print '%'*20
            agents = Agent.objects.all()
            print list(agents)
            for agent in agents:
                notification = Notification(title=instance.title,
                                            content=instance.content,
                                            creator=instance.creator, target=agent.user, date=instance.date)
                notification.save()

            customers = Customer.objects.all()
            print list(customers)
            for customer in customers:
                notification = Notification(title=instance.title,
                                            content=instance.content,
                                            creator=instance.creator, target=customer.user, date=instance.date)
                notification.save()

