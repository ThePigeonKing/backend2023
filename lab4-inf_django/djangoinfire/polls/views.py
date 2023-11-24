from django.shortcuts import render
from django.shortcuts import get_object_or_404, render

from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Question
from .models import Choice
from django.template import loader
from django.views import generic
from django.utils import timezone

class IndexView(generic.ListView):
    template_name = "polls/index.html" # polls/question_list.html by default
    context_object_name = "latest_question_list"
    def get_queryset(self):
        return Question.objects.order_by("-pub_date")[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html" # polls/question_detail.html by default
    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        return render(request,
                      "polls/detail.html",
                      {
                          "question": question,
                          "error_message": "Выберите один из вариантов.",
                      },
                      )
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))