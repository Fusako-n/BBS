from django.urls import path
from . import views

app_name = 'bbs'

urlpatterns = [
    path('', views.index, name='index'),
    path('contacts/', views.contacts, name='contacts'),
    path('reply/<int:pk>/', views.reply, name='reply'),
]