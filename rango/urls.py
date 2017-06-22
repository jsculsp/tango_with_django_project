from django.conf.urls import url
from rango import views, temp


# app_name = 'rango'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^about/', views.about, name='about'),
    url(r'^category/(?P<category_name_slug>[\w\-]+)/$',
        views.show_category, name='show_category'),
    url(r'^add_category/$', views.add_category, name='add_category'),
    url(r'^category/(?P<category_name_slug>[\w\-]+)/add_page/$',
        views.add_page, name='add_page'),
]

urlpatterns += [
    url(r'^test/$', views.test, name='test'),
    url(r'^upload$', views.upload, name='upload'),
]

urlpatterns += [
    url(r'^open/fcoin/order/notify/wepay/$', temp.fcoin_order_notify_wepay, name='fcoin_order_notify_wepay'),
    url(r'^open/fcoin/order/notify/alipay/$', temp.fcoin_order_notify_alipay, name='fcoin_order_notify_alipay'),
]
