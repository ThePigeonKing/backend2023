from django.urls import path
from .views import HomeView, CarListView, CarDetailView, BrandListView, BrandDetailView, CategoryListView, CategoryDetailView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),  
    path('cars/', CarListView.as_view(), name='car_list'),  
    path('cars/<int:pk>/', CarDetailView.as_view(), name='car_detail'),  
    path('brands/', BrandListView.as_view(), name='brand_list'),  
    path('brands/<str:slug>/', BrandDetailView.as_view(), name='brand_detail'),  
    path('categories/', CategoryListView.as_view(), name='category_list'),  
    path('categories/<str:slug>/', CategoryDetailView.as_view(), name='category_detail'), 
]
