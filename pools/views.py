from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.urls import reverse
from django.views import generic
# Create your views here.

from django.http import HttpResponse, Http404, HttpResponseRedirect
from .models import Question, Choice
from django.utils import timezone

class IndexView(generic.ListView):
    template_name = 'pools/index.html'

    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions"""
        #return Question.objects.order_by('-pub_data')[:5]
        """
            Return the last five published questions (not including those set to be
            published in the future).
        """
        return Question.objects.filter(
            pub_data__lte=timezone.now()
        ).order_by('-pub_data')[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = 'pools/detail.html'

    def get_queryset(self):
        """
            Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_data__lte=timezone.now())

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'pools/results.html'

# # Leave the rest of the views (detail, results, vote) unchanged
# def index(request):
#     latest_question_id = Question.objects.order_by('-pub_data')[:5]
#     template = loader.get_template('pools/index.html')
#     context = {'latest_question_list': latest_question_id}
#     #output = ', '.join([q.question_text for q in latest_question_id])
#     #return HttpResponse(template.render(context, request))
#     return render(request, 'pools/index.html', context)
#
# def detail(request, question_id):
#     # try:
#     #     question = Question.objects.get(pk=question_id)
#     # except Question.DoesNotExist:
#     #     raise Http404("Question does not exist")
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'pools/detail.html', {'question': question, })
#     #return HttpResponse("You're looking at question %s" % question_id)
#
# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'pools/results.html', {'question': question})
#     # response = "You're looking at the results of question %s."
#     # return HttpResponse(response % question_id)

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice=question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'pools/detail.html', {'question':question, 'error_message':"You dint' select a choice",})
    else:
        selected_choice.votes += 1
        selected_choice.save()

        return HttpResponseRedirect(reverse('pools:results', args=(question.id, )))
    #return HttpResponse("You're voting on question %s." % question_id)