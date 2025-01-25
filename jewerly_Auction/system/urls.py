from django.urls import path
from . import views

urlpatterns = [
    path('',views.index, name='index'),
    path('valuation/',views.valuation, name='valuation') 
]
