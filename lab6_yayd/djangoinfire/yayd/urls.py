from django.urls import path
from . import views

urlpatterns = [
    # Другие пути
    path('signup/', views.signup, name='signup'),
    path('', views.home, name='home'),
    path('folders/', views.folders_view, name='folders'),
    path('folders/<int:folder_id>/', views.folders_view, name='folders_detail'),
    path('explorer/', views.explorer_view, name='explorer'),
    path('create_folder/', views.create_folder, name='create_folder'),
    path('upload_file/', views.upload_file, name='upload_file'),
    path('view_file/<int:file_id>/', views.view_file, name='view_file'),
    path('delete_file/<int:file_id>/', views.delete_file, name='delete_file'),
    path('delete_folder/<int:folder_id>/', views.delete_folder, name='delete_folder'),
    path('edit_file/<int:file_id>/', views.edit_file, name='edit_file'),
]
