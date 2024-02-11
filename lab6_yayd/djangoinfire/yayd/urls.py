from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('', views.home, name='home'),
    path('folders/', views.folders_view, name='folders'),
    path('folders/<int:folder_id>/', views.folders_view, name='folders_detail'),
    path('explorer/', views.explorer_view, name='explorer'),
    path('create_folder/', views.create_folder, name='create_folder'),
    path('create_folder/<int:folder_id>/', views.create_folder, name='create_folder_with_id'),
    path('upload_file/', views.upload_file, name='upload_file'),
    path('upload_file/<int:folder_id>/', views.upload_file, name='upload_file_with_id'),
    path('view_file/<int:file_id>/', views.view_file, name='view_file'),
    path('delete_file/<int:file_id>/', views.delete_file, name='delete_file'),
    path('delete_folder/<int:folder_id>/', views.delete_folder, name='delete_folder'),
    path('edit_file/<int:file_id>/', views.edit_file, name='edit_file'),
    path('shared_access/', views.shared_access, name='shared_access'),
    path('share_access/<int:object_id>/<str:type>/', views.share_access, name='share_access'),
]
