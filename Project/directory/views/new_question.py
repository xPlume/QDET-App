from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required


from directory.models import Context, Question, Answer
from directory.forms import ContextForm, QuestionForm

from django.forms import modelformset_factory


@login_required
def new_question(request, context_id):
	
	
	context = get_object_or_404(Context, id=context_id)
	
	user = request.user
	
	AnswerFormSet = modelformset_factory(Answer, fields=['answer', 'is_correct'], extra=4)
	prefix = "answers"
	
	
	if request.method == 'POST':
		
		new_question_form = QuestionForm(request.POST)
		answer_formset = AnswerFormSet(request.POST, prefix="answers")
		
		if new_question_form.is_valid() and answer_formset.is_valid():
			
			# Handling the Question (saving later)
			new_question_instance = new_question_form.save(commit=False)
			new_question_instance.uploader = request.user
			new_question_instance.context = context
			
			
			# Handling the answers
			answer_formset_instance = answer_formset.save(commit=False)
			
			# Checking if at least one answer has the is_correct = True
			if not any(instance.is_correct for instance in answer_formset_instance):
				messages.error(request, "You must mark at least one answer as correct.", extra_tags="danger")
				
				return redirect('new_question', context_id)
			#if 
			
			
			
			# If all good, save.
			
			# Saving the Question
			new_question_instance.save()
			
			# Saving the Answers
			for instance in answer_formset_instance:
				instance.question_linked = new_question_instance
				instance.save()
			#for
			
			messages.success(request, "The new question has been added!", extra_tags="success")
			return redirect('single_question', new_question_instance.id)
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
		"new_question_form": new_question_form,
		"answer_formset": answer_formset,
		"prefix": prefix,
	}
	
	return render(request, template_name, context)
	
#def new_question