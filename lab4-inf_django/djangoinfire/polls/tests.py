from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
import datetime
from .models import Question

def create_question(question_text, days):
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)

class QuestionModelTests(TestCase):
    def test_no_questions(self):
        """
        Отображение сообщения при отсутствии вопросов
        """
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Вопросы не найдены.")
        self.assertQuerySetEqual(response.context["latest_question_list"], [])

    def test_past_question(self):
        """
        DetailView опубликованного вопроса содержит его текст
        """
        past_question = create_question(question_text="Past Question.", days=-5)
        url = reverse("polls:detail", args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)

    def test_future_question(self):
        """
        DetailView неопубликованного вопроса возвращает 404.
        """
        future_question = create_question(question_text="Будущий вопрос.", days=5)
        url = reverse("polls:detail", args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
                         
    # def test_future_question_and_past_question(self):
    #     """
    #     Если есть прошлые и будущие вопросы одновременно, показываются прошлые
    #     """
    #     question = create_question(question_text="Прошлый вопрос.", days=-30)
    #     create_question(question_text="Будущий вопрос.", days=30)
    #     response = self.client.get(reverse("polls:index"))
    #     self.assertQuerySetEqual(
    #         response.context["latest_question_list"],
    #         [question],
    #     )

    def test_two_past_questions(self):
        """
        На стартовой странице могут показываться несколько вопросов
        """
        question1 = create_question(question_text="Прошлый вопрос 1.", days=-30)
        question2 = create_question(question_text="Прошлый вопрос 2.", days=-5)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question2, question1],
        )