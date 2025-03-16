from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.get_products, name='get_products'),  # Corrected path
    path('product/<str:product_name>/', views.get_product_details, name='get_product_details'),
    path('search/', views.search_summaries, name='search_summaries'),
]