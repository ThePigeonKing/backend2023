from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from .views import (
    city_detail,
    delete_comment,
    main_page,
    manage_subscriptions,
    register,
    unsubscribe,
    edit_comment,
)

urlpatterns = [
    path("", main_page, name="main_page"),
    path("subscriptions/", manage_subscriptions, name="manage_subscriptions"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path(
        "login/",
        LoginView.as_view(template_name="weather_app/login.html"),
        name="login",
    ),
    path("register/", register, name="register"),
    path("unsubscribe/<int:subscription_id>/", unsubscribe, name="unsubscribe"),
    path("city/<str:city_name>/", city_detail, name="city_detail"),
    path("delete_comment/<int:comment_id>/", delete_comment, name="delete_comment"),
    path('edit_comment/<int:comment_id>/', edit_comment, name='edit_comment'),
]
