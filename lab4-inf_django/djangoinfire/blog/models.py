from django.conf import settings
from django.db import models
from django.urls import reverse
from django import forms
from django.contrib.auth.models import User 

class Post(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Автор"
    )
    title = models.CharField("Заголовок", max_length=200)
    text = models.TextField("Текст")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Пост"
        verbose_name_plural = "Посты"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blog:detail", kwargs={"pk": self.pk})

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', verbose_name="Пост")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Автор комментария")
    text = models.TextField("Текст комментария")
    moderator_text = models.TextField("Комментарий модератора", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_anonymous = models.BooleanField("Анонимный", default=False)
    moderator_text = models.TextField(null=True, blank=True)
    moderator_time = models.DateTimeField(auto_now_add=True)
    show_moderator_text = models.BooleanField(default=False)
    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

    def __str__(self):
        return f'Комментарий от {self.author} к {self.post.title}(id={self.post.id})'



