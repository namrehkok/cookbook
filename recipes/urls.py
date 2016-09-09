from django.conf.urls import url

from . import views

urlpatterns = [
    # ex: /polls/
    #url(r'^$', views.index, name='index'),
    url(r'^list$', views.shoppinglist, name = 'shoppinglist'),
    url(r'^tst$', views.tst, name = 'tst')
    ]
