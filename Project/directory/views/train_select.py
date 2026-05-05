from django.shortcuts import render, redirect
from django.db.models import Prefetch
from django.contrib import messages

from django.contrib.auth.decorators import login_required

from directory.models import Question
from directory.forms import TrainModelForm, SaveTrainedModelForm

from directory.train_model import train_model, save_trained_model_to_db

from types import SimpleNamespace


@login_required
def train_select(request):
	
	user = request.user
	
	model_results = None
	text2props_model = None
	
	if request.method == 'POST':
		
		train_form = TrainModelForm(request.POST)
		save_form = SaveTrainedModelForm(request.POST)
		
		
		if 'train_model' in request.POST:
			
			
			if train_form.is_valid():
				
				# Obtaining the parameters from user selection
				parameter = train_form.cleaned_data['param_selection']
				
				"""
				Parameters: 
				1: Question Difficulty
				2: Question Discrimination
				3: Question Facility
				"""
				
				# Fetching questions with their context and all related answers
				if parameter== '1': # Difficulty
					questions_info = Question.objects.filter(
						uploader=user,
						question_difficulty__isnull=False,
					).select_related('context').prefetch_related('answers').order_by('-id')
				elif parameter== '2': # Discrimination
					questions_info = Question.objects.filter(
						uploader=user,
						question_discrimination__isnull=False,
					).select_related('context').prefetch_related('answers').order_by('-id')
				elif parameter== '3': # Facility
					questions_info = Question.objects.filter(
						uploader=user,
						question_facility__isnull=False,
					).select_related('context').prefetch_related('answers').order_by('-id')
				#if
				
				
				"""
				# Example on how to use the question object
				for question in questions_info:
					print(f"Context: {question.context.context_title}")
					print(f"Question: {question.question}")
					print(f"User: {question.uploader}")
					
					for answer in question.answers.all():
						print(f" - Answer: {answer.answer}")
					#for answers
				#for question
				"""
				
				model_results, text2props_model = train_model(questions_info, parameter)
			#if
			
			
			else: 
				messages.error(request, train_form.errors, extra_tags="danger")
				return redirect('train_select')
			#else
		#if
		
		
		elif 'save_model' in request.POST:
			
			if save_form.is_valid():
				
				# Fields for the db object
				object_info = SimpleNamespace(
					uploader = user,
					title = save_form.cleaned_data['title'],
					public = save_form.cleaned_data['public'],
				)
				
				# Saving the model as pickle file and db object
				save_trained_model_to_db(text2props_model, object_info)
				
			#if
			
			else: 
				messages.error(request, save_form.errors, extra_tags="danger")
				return redirect('train_select')
			#else
		#elif
		
		
		
		
		# return redirect....
		
	#if
	
	else:
		train_form = TrainModelForm()
		save_form = SaveTrainedModelForm()
		model_results = None
	#else
	
	
	
	template_name = "directory/train_select.html"
	context = {
		"train_form": train_form,
		"save_form": save_form,
		"model_results": model_results,
	}
	
	return render(request, template_name, context)
	
#def 