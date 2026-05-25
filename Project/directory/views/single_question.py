# Django imports
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q

# References to other files
from directory.models import Context, Question, Answer, TrainedModel
from directory.decorators import question_creator
from modules.evaluate import evaluate
from modules.histogram_creation import create_histogram
from modules.statistical_metrics import statistical_metrics


@login_required
@question_creator
def single_question(request, question_id):
	
	user = request.user
	
	question = get_object_or_404(Question, id=question_id)
	
	answers = Answer.objects.filter(
		question_linked = question
	)
	
	# Obtaining the users's models
	existing_models = TrainedModel.objects.filter(
		uploader = user,
	)
	
	public_models = TrainedModel.objects.filter(
		public=True,
	).exclude(uploader=user)
	
	
	# Evaluating the question
	if request.method == 'POST':
		
		# Obtaining the IDs of the selected models
		selected_ids = request.POST.getlist('selected_ids')
		
		# Obtaining the question
		questions_info = Question.objects.filter(
			id=question_id
		).select_related('context').prefetch_related('answers').order_by('-id')
		
		
		
		for model_id in selected_ids:
			
			# Double-check that the ID belongs to their own models OR a public model
			is_valid = TrainedModel.objects.filter(id=model_id).filter(
				Q(uploader=user) | Q(public=True),
			).exists()
			
			if is_valid:
				# Query the model
				model_instance = get_object_or_404(TrainedModel, id=model_id)
				
				# Generate the predictions
				evaluate(questions_info, model_instance, user)
				
				# Create and save the Histograms
				create_histogram(model_instance, user)
				
				# Obtain the statisitical metrics of the predicted data set
				statistical_metrics(model_instance, user)
			#if
		#for
		
		messages.success(request, "The evaluations were exectued with success", extra_tags="success")
		return redirect('single_question', question_id)
		
	#if
	
	
	template_name = "directory/single_question.html"
	context = {
		"question": question,
		"answers": answers,
		"existing_models": existing_models,
		"public_models": public_models,
	}
	
	return render(request, template_name, context)
	
#def 