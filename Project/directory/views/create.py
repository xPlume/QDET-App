from django.shortcuts import render, redirect
from django.contrib import messages


from directory.models import Question, Answer
from directory.forms import QuestionForm, AnswerForm


def create(request):
	
	
	if request.method == 'POST':
		
		new_question_form = QuestionForm(request.POST)
		new_answer_form = AnswerForm(request.POST)
		
		if new_question_form.is_valid() and new_answer_form.is_valid():
			
			new_question_instance = new_question_form.save()
			
			new_answer_instance = new_answer_form.save(commit=False)
			new_answer_instance.question_linked = new_question_instance
			new_answer_instance.save()
			
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
		new_answer_form = AnswerForm()
	#else
	
	
	
	
	template_name = "directory/create.html"
	context = {
		"new_question_form": new_question_form,
		"new_answer_form": new_answer_form,
	}
	
	return render(request, template_name, context)
	
#def create