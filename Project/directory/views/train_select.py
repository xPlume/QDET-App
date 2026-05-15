# Django imports
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# References to other files
from directory.models import Question
from directory.forms import TrainModelForm, SaveTrainedModelForm
from directory.train_model import train_model, save_trained_model_to_db

# Others
from types import SimpleNamespace
import codecs
import pickle


@login_required
def train_select(request):
	
	user = request.user
	
	model_results = None
	text2props_model = None
	
	"""
	For this view, saving the loaded model (text2props_model) in a session
	is mandatory. We obtain the model from the train_model, and save it in the
	text2props_model variable. But we thenrefresh the page, losing the values of
	variables - hence the mode, in the process.
	
	By saving the variable in a session, we preserve its value, allowing us to retrieve
	it and properly save it even after a page refresh.
	"""
	
	
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
				
				
				# Cache the model in the session
				# We serialize it to a base64 string so Django sessions can safely store it
				serialized_model = codecs.encode(pickle.dumps(text2props_model), "base64").decode("utf-8")
				request.session['temporary_trained_model'] = serialized_model
				
			#if
			
			
			else: 
				messages.error(request, train_form.errors, extra_tags="danger")
				return redirect('train_select')
			#else
		#if
		
		
		elif 'save_model' in request.POST:
			
			if save_form.is_valid():
				
				# Retrieve the model from the session
				serialized_model = request.session.get('temporary_trained_model')
				
				
				if serialized_model:
					# De-serialize back into a Python object
					text2props_model = pickle.loads(codecs.decode(serialized_model.encode(), "base64"))
					
					object_info = SimpleNamespace(
						uploader=user,
						title=save_form.cleaned_data['title'],
						public=save_form.cleaned_data['public'],
					)
					
					# Saving the model as pickle file and db object
					save_trained_model_to_db(text2props_model, object_info)
					
					# Clean up session memory now that it's safe in the permanent DB
					del request.session['temporary_trained_model']
					
					messages.success(request, "The model was saved with success", extra_tags="success")
					return redirect('user_questions')
				#if 
				else:
					messages.error(request, "Training session expired or model not found. Please train again.", extra_tags="danger")
					return redirect('train_select')
				#else
				
				
			#if
			
			else: 
				messages.error(request, save_form.errors, extra_tags="danger")
				return redirect('train_select')
			#else
		#elif
		
		
	#if
	
	else:
		train_form = TrainModelForm()
		save_form = SaveTrainedModelForm()
	#else
	
	
	
	template_name = "directory/train_select.html"
	context = {
		"train_form": train_form,
		"save_form": save_form,
		"model_results": model_results,
	}
	
	return render(request, template_name, context)
	
#def 