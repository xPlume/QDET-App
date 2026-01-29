from django.shortcuts import render, get_object_or_404

from django.contrib.auth.decorators import login_required

from directory.models import Question, Answer


@login_required
def single_question(request, question_id):
	
	user = request.user
	
	question = get_object_or_404(Question, id=question_id)
	
	answers = Answer.objects.filter(
		question_linked = question
	)
	
	
	template_name = "directory/single_question.html"
	context = {
		"question": question,
		"answers": answers,
	}
	
	return render(request, template_name, context)
	
#def 