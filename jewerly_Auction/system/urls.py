from django.urls import path
from . import views

urlpatterns = [
    path('',views.index, name='index'),
    path('valuation/',views.diamond_valuation_view, name='valuation'),
    path('print/', views.print_valuation_view, name='print_valuation'),
]
