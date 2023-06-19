from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Question, Choice
from django.views import generic
from django.utils import timezone

# Vistas con funciones.

# def index(request):
#     latest_question_list= Question.objects.all()
#     return render(request,"polls/index.html",{
#         "latest_question_list": latest_question_list
#     })

# def detail(request,question_id):
#     question = get_object_or_404(Question,pk=question_id)
#     return render(request,"polls/detail.html",{
#         "question":question
#     })
    # return HttpResponse(f"Estás viendo la pregunta número: {question_id}")

# def result(request,question_id):
#     question = get_object_or_404(Question,pk= question_id )
#     return render(request,"polls/result.html",{
#         "question":question
#     })
    # return HttpResponse(f"Estás viendo los resultados de la pregunta número:  {question_id}")

#Vistas con clases:
class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """Return the last five published questions"""
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:5]
# __lte es un método que significa less than now time

class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"

    def get_queryset(self):
        """
        Excludes any question that arent published yet
        """
        return Question.objects.filter(pub_date__lte=timezone.now())
    #restrinjo las peguntas para que no se vean las del futuro


class ResultView(generic.DetailView):
    model = Question
    template_name = "polls/result.html"
    

def vote(request,question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk= request.POST["choice"])
        #choice hace referencia al name del input
    except(KeyError,Choice.DoesNotExist):
        return render(request, "polls/detail.html",{
            "question":question,
            "error_message":"No elegiste una respuesta"
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse("polls:result",args=(question.id,)))

