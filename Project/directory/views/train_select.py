from django.shortcuts import render
from django.db.models import Prefetch

from django.contrib.auth.decorators import login_required

from directory.models import Question
from directory.forms import TrainModelForm

from directory.train_model import train_model

from types import SimpleNamespace


@login_required
def train_select(request):
	
	user = request.user
	
	
	if request.method == 'POST':
		
		form = TrainModelForm(request.POST)
		
		if form.is_valid():
			object_info = SimpleNamespace(
				uploader = user,
				title = form.cleaned_data['title'],
				public = form.cleaned_data['public'],
				param_type = form.cleaned_data['param_selection'],
			)
		#if
		
		"""
		Parameters: 
		1: Question Difficulty
		2: Question Discrimination
		3: Question Facility
		"""
		
		# Fetching questions with their context and all related answers
		if object_info.param_type== '1': # Difficulty
			questions_info = Question.objects.filter(
				uploader=user,
				question_difficulty__isnull=False,
			).select_related('context').prefetch_related('answers').order_by('-id')
		elif object_info.param_type== '2': # Discrimination
			questions_info = Question.objects.filter(
				uploader=user,
				question_discrimination__isnull=False,
			).select_related('context').prefetch_related('answers').order_by('-id')
		elif object_info.param_type== '3': # Facility
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
		
		train_model(questions_info, object_info)
		
		# return redirect....
		
	#if
	
	
	template_name = "directory/train_select.html"
	context = {
		
	}
	
	return render(request, template_name, context)
	
#def 