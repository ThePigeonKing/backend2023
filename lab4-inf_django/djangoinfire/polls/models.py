import datetime

from django.db import models
from django.utils import timezone
from django.contrib import admin

class Question(models.Model):
    question_text = models.CharField("Вопрос", max_length=200)
    pub_date = models.DateTimeField('Дата публикации')
    def __str__(self):
        return self.question_text
    
    @admin.display(
        boolean=True,
        ordering="pub_date",
        description="Опубликован недавно?",
    )
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
    
    def get_queryset(self):
        return Question.objects.filter(
            pub_date__lte=timezone.now()).order_by("-pub_date")[:5]

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField("Ответ", max_length=200)
    votes = models.IntegerField("Количество голосов", default=0)
    def __str__(self):
        return self.choice_text
    
