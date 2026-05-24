from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from directory.models import TrainedModel


@login_required
def evaluations(request):
	
	user = request.user
	
	evaluations = TrainedModel.objects.prefetch_related('histograms', 'statistics').all().order_by('-id')
	
	template_name = "directory/evaluations.html"
	context = {
		"user": user,
		"evaluations": evaluations,
	}
	
	return render(request, template_name, context)
	
#def index