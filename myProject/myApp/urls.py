from django.urls import path
from . import views

urlpatterns = [
    # Root API endpoint
    path('', views.api_root, name='api_root'),
    
    # Basic API endpoint
    path('api/hello/', views.hello_api, name='hello_api'),
    
    # API endpoint that handles GET with query parameters
    path('api/greet/', views.greet_api, name='greet_api'),
    
    # API endpoint for handling POST requests
    path('api/submit/', views.submit_api, name='submit_api'),
    
    # API endpoint handling both GET and POST
    path('api/combined/', views.combined_api, name='combined_api'),
    
    # Item API endpoints
    path('api/items/', views.items_list, name='items_list'),
    path('api/items/add/', views.add_item, name='add_item'),
    path('api/items/<int:item_id>/', views.item_detail, name='item_detail'),
    path('api/items/update/<int:item_id>/', views.update_item, name='update_item'),
    path('api/items/delete/<int:item_id>/', views.delete_item, name='delete_item'),
] 