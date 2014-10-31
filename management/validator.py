from django.core.exceptions import ValidationError
import re
from django.utils.translation import ugettext as _


def validate_mac(value):
    mac_re = r'^([0-9a-fA-F]{2}([:-]?|$)){6}$'
    if re.match(mac_re, value):
        pass
    else:
        raise ValidationError(_('Invalid MAC Address'))


def validate_phone(value):
    phone_re = r'^([0-9]){11}$'
    if re.match(phone_re, value):
        pass
    else:
        raise ValidationError(_('Invalid Phone Number'))
