from django.shortcuts import render
from django.core.paginator import Paginator


from directory.models import Context, Question

def index(request):
	
	user = request.user
	
	nb_context = Context.objects.filter(
		uploader = user
	).order_by('-id').count()
	
	nb_questions = Question.objects.filter(
		uploader = user
	).order_by('-id').count()
	
	
	# Restricting the queryset to 4 object, not more
	questions = Question.objects.filter(
		uploader = user
	).order_by('-id')[:4]
	
	
	template_name = "directory/index.html"
	context = {
		"user": user,
		"nb_context": nb_context,
		"nb_questions": nb_questions,
		"questions": questions,
	}
	
	return render(request, template_name, context)
	
#def index