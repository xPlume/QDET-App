from django.shortcuts import render
from django.core.paginator import Paginator


from directory.models import Context, Question, TrainedModel, Histogram, Statistic

def index(request):
	
	# User not logged in
	if not request.user.is_authenticated:
		# return specific HTML document
		template_name = "directory/index_not_logged_in.html"
		context = {}
		return render(request, template_name, context)
	#if
	
	# else, user is logged in
	
	user = request.user
	
	nb_context = Context.objects.filter(
		uploader = user
	).count()
	
	nb_questions = Question.objects.filter(
		uploader = user
	).count()
	
	nb_model = TrainedModel.objects.filter(
		uploader = user,
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
	
	# Obtaning recent evaluations
	statistics = Statistic.objects.filter(
		user = user
	).order_by('-id')[:4]
	
	nb_statistics = Statistic.objects.filter(
		user = user
	).count()
	
	template_name = "directory/index.html"
	context = {
		"user": user,
		"nb_context": nb_context,
		"nb_questions": nb_questions,
		"nb_model": nb_model,
		"questions": questions,
		"histograms": histograms,
		"nb_histograms": nb_histograms,
		"statistics": statistics,
		"nb_statistics": nb_statistics,
	}
	
	return render(request, template_name, context)
	
#def index