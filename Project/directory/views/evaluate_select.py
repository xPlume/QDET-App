from django.shortcuts import render, get_object_or_404
from django.db.models import Prefetch

from django.contrib.auth.decorators import login_required

from directory.models import Question, TrainedModel

from directory.evaluate import evaluate


@login_required
def evaluate_select(request):
	
	user = request.user
	
	# Obtaining the users's models
	existing_models = TrainedModel.objects.filter(
		uploader = user,
	)
	
	
	# Obtaining the selected model
	if request.method == 'POST':
		# Get the ID string from the <select> name attribute
		selected_id = request.POST.get('param_selection')
		
		if selected_id:
			
			# Obtaining the users's questions
			questions_info = Question.objects.filter(
				uploader=user,
			).select_related('context').prefetch_related('answers').order_by('-id')
			
			
			# Query the model
			model_instance = get_object_or_404(TrainedModel, id=selected_id, uploader=user)
			
			# Calling the evaluate function
			evaluate(questions_info, model_instance)
			
			# return redirect...
			
		#if
	#if
	
	
	
	
	template_name = "directory/evaluate_select.html"
	context = {
		"existing_models": existing_models,
	}
	
	return render(request, template_name, context)
	
#def 