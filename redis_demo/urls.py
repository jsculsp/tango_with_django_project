from django.conf.urls import url

from redis_demo import views

# app_name = 'redis_demo'
urlpatterns = [
    url(r'^$', views.index, name='redis-demo_index'),
]
