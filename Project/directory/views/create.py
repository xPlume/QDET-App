from django.shortcuts import render, redirect
from django.contrib import messages


from directory.models import Question, Answer
from directory.forms import QuestionForm, AnswerForm

from django.forms import modelformset_factory


def create(request):
	
	AnswerFormSet = modelformset_factory(Answer, fields=['answer', 'is_correct'], extra=1)
	
	if request.method == 'POST':
		
		new_question_form = QuestionForm(request.POST)
		answer_formset = AnswerFormSet(request.POST, prefix="answers")
		
		if new_question_form.is_valid() and answer_formset.is_valid():
			
			new_question_instance = new_question_form.save()
			
			# Handling the answers
			answer_formset_instance = answer_formset.save(commit=False)
			for instance in answer_formset_instance:
				instance.question_linked = new_question_instance
				instance.save()
			#for
			
			messages.success(request, "The new question has been added!", extra_tags="success")
			return redirect('index')
		#if
		
		else:
			messages.error(request, new_question_form.errors, extra_tags="danger")
			return redirect('create')
		#else
		
	#if
	
	else:
		new_question_form = QuestionForm()
		answer_formset = AnswerFormSet(queryset=Answer.objects.none(), prefix="answers")
	#else
	
	
	
	
	template_name = "directory/create.html"
	context = {
		"new_question_form": new_question_form,
		"answer_formset": answer_formset,
	}
	
	return render(request, template_name, context)
	
#def create