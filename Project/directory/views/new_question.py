from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required


from directory.models import Context, Question, Answer, TopicNames, Topics
from directory.forms import ContextForm, QuestionForm, TopicsForm

from django.forms import modelformset_factory


@login_required
def new_question(request, context_id):
	
	
	context = get_object_or_404(Context, id=context_id)
	
	user = request.user
	existing_topics = TopicNames.objects.filter(
		user=user,
	)
	
	AnswerFormSet = modelformset_factory(Answer, fields=['answer', 'is_correct'], extra=4)
	prefix = "answers"
	
	
	if request.method == 'POST':
		
		new_question_form = QuestionForm(request.POST)
		new_topic_form = TopicsForm(request.POST)
		answer_formset = AnswerFormSet(request.POST, prefix="answers")
		
		if new_question_form.is_valid() and new_topic_form.is_valid() and answer_formset.is_valid():
			
			# Handling the Question (saving later)
			new_question_instance = new_question_form.save(commit=False)
			new_question_instance.uploader = request.user
			new_question_instance.context = context
			
			# Handling topics
			new_topic_instance = new_topic_form.save(commit=False)
			selected_topic_id = request.POST.get('topic_selection')
			if selected_topic_id: # If a topic is selected
				topic_object = get_object_or_404(TopicNames, id=selected_topic_id)
				new_topic_instance.topic_name = topic_object
				new_topic_instance.question = new_question_instance
			#
			
			
			
			
			# Handling the answers
			answer_formset_instance = answer_formset.save(commit=False)
			
			# Checking if at least one answer has the is_correct = True
			if not any(instance.is_correct for instance in answer_formset_instance):
				messages.error(request, "You must mark at least one answer as correct.", extra_tags="danger")
				
				return redirect('new_question', context_id)
			#if 
			
			
			
			# If all good, save.
			
			# Saving the Question & Topic
			new_question_instance.save()
			if selected_topic_id:
				new_topic_instance.save()
			#if
			
			# Saving the Answers
			for instance in answer_formset_instance:
				instance.question_linked = new_question_instance
				instance.save()
			#for
			
			messages.success(request, "The new question has been added!", extra_tags="success")
			return redirect('index')
		#if
		
		else:
			messages.error(request, new_question_form.errors, extra_tags="danger")
			return redirect('new_question', context_id)
		#else
		
	#if
	
	else:
		new_question_form = QuestionForm()
		answer_formset = AnswerFormSet(queryset=Answer.objects.none(), prefix="answers")
	#else
	
	
	
	
	template_name = "directory/new_question.html"
	context = {
		"context": context,
		"existing_topics": existing_topics,
		"new_question_form": new_question_form,
		"answer_formset": answer_formset,
		"prefix": prefix,
	}
	
	return render(request, template_name, context)
	
#def new_question