from django.urls import path
from . import views

urlpatterns = [
    path('',views.index, name='index'),
    path('valuation/',views.diamond_valuation_view, name='valuation'),
    # path('print_valuation/', views.print_valuation_view, name='print_valuation'),
    path('Request_table/', views.valuation_request_list, name='Request_table'),
    path('delete_request/<int:request_id>/', views.delete_request, name='delete_request'),
    path('send_request/<int:request_id>/', views.send_request, name='send_request'),
    
]
