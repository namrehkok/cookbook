from django.conf.urls import url

from . import views

urlpatterns = [
    # ex: /polls/
    #url(r'^$', views.index, name='index'),
    url(r'^shoppinglist$', views.shoppinglist, name = 'shoppinglist')
    ]
