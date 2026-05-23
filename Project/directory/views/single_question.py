# Django imports
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# References to other files
from directory.models import Context, Question, Answer, TrainedModel
from directory.decorators import question_creator
from modules.evaluate import evaluate


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
	
	# Evaluating the question
	if request.method == 'POST':
		
		# Obtaining the IDs of the selected models
		selected_ids = request.POST.getlist('selected_ids')
		
		# Obtaining the question
		questions_info = Question.objects.filter(
			id=question_id
		).select_related('context').prefetch_related('answers').order_by('-id')
		
		for model_id in selected_ids:
			# Query the model
			model_instance = get_object_or_404(TrainedModel, id=model_id, uploader=user)
			
			# Calling the evaluate function
			evaluate(questions_info, model_instance, user)
		#for
		
		messages.success(request, "The evalutaion was exectued with success", extra_tags="success")
		return redirect('single_question', question_id)
		
	#if
	
	
	template_name = "directory/single_question.html"
	context = {
		"question": question,
		"answers": answers,
		"existing_models": existing_models,
	}
	
	return render(request, template_name, context)
	
#def 