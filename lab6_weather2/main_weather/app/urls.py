# app/urls.py
from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('search/', views.search_weather, name='weather_search'),
    path('weather/<str:city_name>/', views.weather_details, name='weather_details'),
    path('forecast/<str:city_name>/', views.weather_forecast, name='weather_forecast'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('subscribe/<str:city_name>/', views.subscribe_to_city, name='subscribe_city'),
    path('unsubscribe/<str:city_name>/', views.unsubscribe_from_city, name='unsubscribe_city'),
    path('observations/add/<int:location_id>/', views.add_observation, name='add_observation'),
    path('observations/edit/<int:observation_id>/', views.edit_observation, name='edit_observation'),
    path('observations/delete/<int:observation_id>/', views.delete_observation, name='delete_observation'),
]