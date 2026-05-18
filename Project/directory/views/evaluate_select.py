# Django imports
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Prefetch
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Referece to other files
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
		# Obtaining the ID of the selected model
		selected_id = request.POST.get('param_selection')
		
		if selected_id:
			
			# Obtaining the users's questions
			questions_info = Question.objects.filter(
				uploader=user,
			).select_related('context').prefetch_related('answers').order_by('id')
			
			
			# Query the model
			model_instance = get_object_or_404(TrainedModel, id=selected_id, uploader=user)
			
			# Calling the evaluate function
			evaluate(questions_info, model_instance, user)
			
			messages.success(request, f"Successfully evaluated all the questions.", extra_tags="success")
			return redirect('index')
			
		#if
	#if
	
	
	
	
	template_name = "directory/evaluate_select.html"
	context = {
		"existing_models": existing_models,
	}
	
	return render(request, template_name, context)
	
#def 