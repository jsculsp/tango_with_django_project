from django.apps import AppConfig
# from django.db.models.signals import pre_save
# from django.dispatch import receiver
#
# from utils import log


class Count(object):
    n = 0
count = Count()


class RangoConfig(AppConfig):
    name = 'rango'