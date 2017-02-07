from django.dispatch import receiver
from django.core.signals import request_finished
from django.db.models.signals import pre_save

from rango.models import Category
from utils import log

__all__ = ['signal_request_times', 'signal_category_to_save']

class Count(object):
    n = 0
count = Count()


@receiver(request_finished)
def signal_request_times(sender, **kwargs):
    count.n += 1
    if count.n > 1:
        log('You have requested for {} times'.format(count.n))
    else:
        log('You have requested for {} time'.format(count.n))


@receiver(pre_save, sender=Category)
def signal_category_to_save(sender, **kwargs):
    log('Your Category model is to be saved...')