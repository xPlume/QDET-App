# Django imports
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.db.models import Q

# References to other files
from directory.models import TrainedModel, Question
from modules.evaluate import evaluate
from modules.histogram_creation import create_histogram
from modules.statistical_metrics import statistical_metrics


@login_required
def evaluations(request):
	
	user = request.user
	
	evaluations = TrainedModel.objects.prefetch_related('histograms', 'statistics').filter(
		uploader = user,
	).order_by('-id')
	
	public_models = TrainedModel.objects.prefetch_related('histograms', 'statistics').filter(
		public = True,
	).order_by('-id')
	
	
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
			
			# Generate the predictions
			evaluate(questions_info, model_instance, user)
			
			# Create and save the Histograms
			create_histogram(model_instance, user)
			
			# Obtain the statisitical metrics of the predicted data set
			statistical_metrics(model_instance, user)
			
			
			messages.success(request, f"Successfully evaluated all the questions.", extra_tags="success")
			
			base_url = reverse('evaluations')
			redirect_url = f"{base_url}?scroll={model_instance.id}"
			return redirect(redirect_url)
		#if
		else:
			messages.error(request, f"An error occured.", extra_tags="danger")
			return redirect('evaluations')
		#else
	#if
	
	
	template_name = "directory/evaluations.html"
	context = {
		"evaluations": evaluations,
		"public_models": public_models,
	}
	
	return render(request, template_name, context)
	
#def index