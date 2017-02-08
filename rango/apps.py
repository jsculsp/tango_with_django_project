from django.apps import AppConfig
from django.db.models.signals import pre_save
from django.dispatch import receiver

from utils import log


class Count(object):
    n = 0
count = Count()


class RangoConfig(AppConfig):
    name = 'rango'

    def ready(self):
        Category = self.get_model('Category')
        @receiver(pre_save, sender=Category)
        def signal_category_to_save(sender, **kwargs):
            log('Your Category model is to be saved...')