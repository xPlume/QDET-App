from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from directory.models import Question, Answer
from directory.forms import QuestionForm
from directory.decorators import question_creator


@login_required
@question_creator
def update_question(request, question_id):
	
	user = request.user
	
	question = get_object_or_404(Question, id=question_id)
	
	answers = Answer.objects.filter(
		question_linked = question
	)
	
	
	
	if request.method == 'POST':
		
		update_question = QuestionForm(request.POST, instance=question)
		
		
		if update_question.is_valid():
			
			update_instance = update_question.save(commit=False)
			update_instance.uploader = request.user
			update_instance.save()
			
			messages.success(request, "The MCQ was updated with success!", extra_tags="success")
			return redirect('single_question', question_id)
		#if
		
		else:
			messages.error(request, update_question.errors, extra_tags="danger")
			return redirect('update_question', question_id)
		#else
		
		
	#if
	
	else:
		update_question = QuestionForm(instance=question)
	#else
	
	
	template_name = "directory/update_question.html"
	context = {
		"question": question,
		"answers": answers,
		"update_question": update_question,
	}
	
	return render(request, template_name, context)
	
#def 