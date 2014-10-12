from django.contrib import admin
from models import (Notification, Gateway, WifiClient, Ad, AdStat)

admin.site.register(Notification)
admin.site.register(Gateway)
admin.site.register(WifiClient)
admin.site.register(Ad)
admin.site.register(AdStat)

