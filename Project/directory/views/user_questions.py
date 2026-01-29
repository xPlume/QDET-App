from django.shortcuts import render

from django.contrib.auth.decorators import login_required

from directory.models import Question


@login_required
def user_questions(request):
	
	user = request.user
	
	questions = Question.objects.filter(
		uploader = user
	)
	
	
	template_name = "directory/user_questions.html"
	context = {
		"questions": questions,
	}
	
	return render(request, template_name, context)
	
#def 