from django.urls import path
from . import views

app_name = 'bbs'

urlpatterns = [
    path('', views.index, name='index'),
    path('contacts/', views.contacts, name='contacts'),
    path('reply/<int:pk>/', views.reply, name='reply'),
    path('topic_delete/<int:pk>/', views.topic_delete, name='topic_delete'),
    path('topic_edit/<int:pk>/', views.topic_edit, name='topic_edit'),
]