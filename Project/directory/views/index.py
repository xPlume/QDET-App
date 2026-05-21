from django.shortcuts import render
from django.core.paginator import Paginator


from directory.models import Context, Question, Histogram

def index(request):
	
	user = request.user
	
	nb_context = Context.objects.filter(
		uploader = user
	).count()
	
	nb_questions = Question.objects.filter(
		uploader = user
	).count()
	
	
	# Restricting the queryset to 4 object, not more
	questions = Question.objects.filter(
		uploader = user
	).order_by('-id')[:4]
	
	# Obtaining latest 2 histograms
	histograms = Histogram.objects.filter(
		user = user
	).order_by('-id')[:2]
	
	nb_histograms = Histogram.objects.filter(
		user = user
	).count()
	
	template_name = "directory/index.html"
	context = {
		"user": user,
		"nb_context": nb_context,
		"nb_questions": nb_questions,
		"questions": questions,
		"histograms": histograms,
		"nb_histograms": nb_histograms,
	}
	
	return render(request, template_name, context)
	
#def index