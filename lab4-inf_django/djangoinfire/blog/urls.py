from django.urls import path

from . import views

app_name = "blog"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    path("post/new/", views.CreateView.as_view(), name="post_new"),
    path("post/edit/<int:pk>", views.UpdateView.as_view(), name="post_edit"),
    path("post/delete/<int:pk>", views.DeleteView.as_view(), name="post_delete"),
    path('blog/post/<int:pk>/comment/create', views.CommentCreateView.as_view(), name='comment_create'),
    path("comment/more/<int:pk>", views.CommentMoreView.as_view(), name="comment_more"),
    path("comment/more/edit/<int:pk>", views.CommentUpdateView.as_view(), name="comment_edit"),
    path("comment/more/delete/<int:pk>", views.CommentDeleteView.as_view(), name="comment_delete"),
]
