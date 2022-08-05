from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Question, Choice
from django.template import loader
from django.http import Http404
from django.urls import reverse

# Create your views here.


def index(request):
	latest_question_list = Question.objects.order_by('-pub_date')[:5]
	context = {'latest_question_list' : latest_question_list}
	return render(request, 'polls/index.html', context)  #render is shortcut
    # return HttpResponse("Hello, world. You're at the polls index.")

	# template = loader.get_template('polls/index.html')
	# return HttpResponse(template.render(context, request))

    # output = ', '.join([q.question_text for q in latest_question_list])
    # return HttpResponse(output)




def detail(request, question_id):
	# try:
	# 	question = Question.objects.get(pk=question_id)
	# except Question.DoesNotExist:
	# 	raise Http404("Question does not exist")

	question = get_object_or_404(Question, pk=question_id)  #shortcut for raise Http404

	return render(request,'polls/detail.html', {'question':question})
    # return HttpResponse("You're looking at question %s." % question_id)

def results(request, question_id):
    # response = "You're looking at the results of question %s."
    # return HttpResponse(response % question_id)
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})

def vote(request, question_id):
    # return HttpResponse("You're voting on question %s." % question_id)

    question = get_object_or_404(Question, pk = question_id)
    if(request.POST['action']=="Clear Votes"):
    	for c in question.choice_set.all():
    		c.votes = 0
    		c.save()
    	return HttpResponseRedirect(reverse('polls:detail',args=(question_id,)))
    else:
	    try:
	    	selected_choice = question.choice_set.get(pk=request.POST['choice'])
	    except (KeyError, choice.DoesNotExist):
	    	#Redisplay the question voting form.
	    	return render(request, 'polls/detail.html', {
	    		'question':question,
	    		'error_message': "You didn't select a choice.",
	    		})
	    else:
	    	if (selected_choice.choice_text=="Backend"):
	    		subq(request, question_id)
	    	else:
		    	selected_choice.votes += 1
		    	selected_choice.save()
		    	#HttpResponseRedirect prevents data from being posted
		    	#twice if a user hits the Back button.
		    	return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))



def subq(request, question_id):

	try:
		selected_choice = question.choice_set.get(pk=request.POST['choice'])
	except (KeyError, choice.DoesNotExist):
		#Redisplay the question voting form.
		return render(request, 'polls/detail.html', {
    		'question':question,
    		'error_message': "You didn't select a choice.",
    		})
	else:
		selected_choice.votes += 1
		selected_choice.save()
    	#HttpResponseRedirect prevents data from being posted
    	#twice if a user hits the Back button.
		return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

