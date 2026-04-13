from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import Prefetch

from django.contrib.auth.decorators import login_required

from directory.models import Question

from text2props.example_model_2 import runner


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
	
	
	# Evaluting the questions
	if request.method == 'POST':
		# Fetching questions with their context and all related answers
		questions_info = Question.objects.filter(
			uploader=user, 
			question_facility__isnull=False
		).select_related('context').prefetch_related('answers').order_by('-id')
		
		"""
		for question in questions_info:
			print(f"Context: {question.context.context_title}")
			print(f"Question: {question.question}")
			
			for answer in question.answers.all():
				print(f" - Answer: {answer.answer}")
			#for answers
		#for question
		"""
		
		
		runner(questions_info)
	#if
	
	
	template_name = "directory/user_questions.html"
	context = {
		"page_obj": page_obj,
	}
	
	return render(request, template_name, context)
	
#def 