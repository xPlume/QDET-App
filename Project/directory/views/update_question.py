from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from directory.models import Question, Answer
from directory.forms import QuestionForm
from directory.decorators import question_creator

from django.forms import modelformset_factory


@login_required
@question_creator
def update_question(request, question_id):
	
	user = request.user
	
	question = get_object_or_404(Question, id=question_id)
	
	answers = Answer.objects.filter(
		question_linked = question
	)
	
	
	AnswerFormSet = modelformset_factory(Answer, fields=['answer', 'is_correct'], can_delete=True, extra=1)
	
	if request.method == 'POST':
		
		update_question = QuestionForm(request.POST, instance=question)
		answer_formset = AnswerFormSet(request.POST, queryset=answers)
		
		if update_question.is_valid() and answer_formset.is_valid():
			
			# Updating question
			update_instance = update_question.save(commit=False)
			update_instance.uploader = request.user
			update_instance.save()
			
			
			# Updating answers
			submitted_answer_formset = answer_formset.save(commit=False)
			for element in submitted_answer_formset:
				element.question_linked = question
				element.save()
			#for
			
			# If answers are deleted
			for element in answer_formset.deleted_objects:
				element.delete()
			#for
			
			messages.success(request, "The MCQ was updated with success!", extra_tags="success")
			return redirect('single_question', question_id)
		#if
		
		else:
			messages.error(request, answer_formset.errors, extra_tags="danger")
			return redirect('update_question', question_id)
		#else
		
		
	#if
	
	else:
		update_question = QuestionForm(instance=question)
		answer_formset = AnswerFormSet(queryset=answers)
	#else
	
	
	template_name = "directory/update_question.html"
	context = {
		"question": question,
		"answers": answers,
		"update_question": update_question,
		"answer_formset": answer_formset,
	}
	
	return render(request, template_name, context)
	
#def 