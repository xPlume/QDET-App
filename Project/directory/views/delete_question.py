# Django imports
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Referencing other files
from directory.models import Question
from directory.decorators import question_creator


@login_required
@question_creator
def delete_question(request, question_id):
	
	
	question = get_object_or_404(Question, id=question_id)
	
	
	if request.method == 'POST':
		
		question.delete()
		messages.success(request, "The question has been successfully deleted.", extra_tags="success")
		return redirect("index")
		
	#if
	
	
#def create
