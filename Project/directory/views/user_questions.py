from django.shortcuts import render
from django.core.paginator import Paginator

from django.contrib.auth.decorators import login_required

from directory.models import Question


@login_required
def user_questions(request):
	
	user = request.user
	
	questions = Question.objects.filter(
		uploader = user
	).order_by('-id')
	
	# Restricting the queryset to 50 object, not more
	paginator = Paginator(questions, 50)
	
	
	# Get the page number from the URL (e.g., ?page=2)
	page_number = request.GET.get('page')
	
	# Get the specific page object
	page_obj = paginator.get_page(page_number)
	
	
	
	template_name = "directory/user_questions.html"
	context = {
		"page_obj": page_obj,
	}
	
	return render(request, template_name, context)
	
#def 