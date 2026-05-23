# Django imports
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Prefetch
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q

# Reference to other files
from directory.models import Question, TrainedModel
from modules.evaluate import evaluate


@login_required
def evaluate_select(request):
	
	user = request.user
	
	# Obtaining the users's models
	user_models = TrainedModel.objects.filter(
		uploader = user,
	)
	
	public_models = TrainedModel.objects.filter(
		public=True,
	).exclude(uploader=user)
	
	
	# Obtaining the selected model
	if request.method == 'POST':
		# Obtaining the ID of the selected model
		selected_id = request.POST.get('param_selection')
		
		# Double-check that the ID belongs to their own models OR a public model
		is_valid = TrainedModel.objects.filter(id=selected_id).filter(
			Q(uploader=user) | Q(public=True),
		).exists()
		
		
		
		if is_valid:
			# Obtaining the users's questions
			questions_info = Question.objects.filter(
				uploader=user,
			).select_related('context').prefetch_related('answers').order_by('id')
			
			
			# Query the model
			model_instance = get_object_or_404(TrainedModel, id=selected_id)
			
			# Calling the evaluate function
			evaluate(questions_info, model_instance, user)
			
			messages.success(request, f"Successfully evaluated all the questions.", extra_tags="success")
			return redirect('index')
			
		#if
		else:
			messages.error(request, f"An error occured, please try again", extra_tags="danger")
			return redirect('evaluate_select')
		#else
		
	#if
	
	
	
	
	template_name = "directory/evaluate_select.html"
	context = {
		"user_models": user_models,
		"public_models": public_models,
	}
	
	return render(request, template_name, context)
	
#def 