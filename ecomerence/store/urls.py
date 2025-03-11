from django.urls import path
from . import views

urlpatterns = [
    path('', views.store, name='store'),  # Handles the `/store/` URL
    path('product/<slug:slug>/',views.product_info, name='product-info'),
    path('category/<slug:category_slug>/', views.list_category, name='list-category'),  # Fix here
]

