# classification/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('classify/', views.classify, name='classify'),
]
