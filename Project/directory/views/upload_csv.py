# Libraries
import csv
import io
from decimal import Decimal, InvalidOperation

# Django imports
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import transaction
from django.contrib.auth.decorators import login_required

# Referencing other files
from directory.forms import CSVuploadForm
from directory.models import Context, Question, Answer
from directory.utils import safe_decimal


@login_required
def upload_csv(request):
	user = request.user

	if request.method == 'POST':
		form = CSVuploadForm(request.POST, request.FILES)
		
		if form.is_valid():
			csv_file = request.FILES['file']
			
			# Use utf-8-sig to handle potential BOM from Excel
			decoded_file = csv_file.read().decode('utf-8-sig')
			io_string = io.StringIO(decoded_file)
			
			# CHANGED: Use DictReader instead of csv.reader. 
			# It automatically reads the first row as headers.
			reader = csv.DictReader(io_string, delimiter=',')
			
			try:
				with transaction.atomic():
					count = 0
					
					# CHANGED: DictReader doesn't support direct indexing, 
					# so we track the row index manually for error reporting.
					for row_index, row in enumerate(reader, start=1):

						# 1. Basic Validation - Mapped exactly to your CSV headers
						required_fields = ['context_id', 'target_level', 'q_id', 'question', 'correct_answer']
						
						# Ensure all required headers exist and have a non-empty value in this row
						if not all(row.get(field) for field in required_fields):
							# Tip: You can print() or log here during debugging to see skipped rows
							# print(f"Skipping row {row_index} due to missing required fields.")
							continue
						
						# 2. Extract Data using exact CSV header strings
						context_id = row.get('context_id')
						context_title = row.get('context_title')
						context_text = row.get('text')  # Changed from 'context_text' to 'text'
						target_level = row.get('target_level')
						q_id = row.get('q_id')
						question_text = row.get('question')  # Changed from 'question_text' to 'question'
						
						# Safely handle missing optional metric columns
						raw_diff = row.get('question_difficulty')
						question_difficulty = safe_decimal(raw_diff, places=2) if raw_diff else None
						
						raw_disc = row.get('question_discrimination')
						question_discrimination = safe_decimal(raw_disc, places=3) if raw_disc else None
						
						raw_fac = row.get('question_facility')
						question_facility = safe_decimal(raw_fac, places=3) if raw_fac else None
						
						# Options data mapped to your option_0 through option_3 headers
						options_data = [
							row.get('option_0'), 
							row.get('option_1'), 
							row.get('option_2'), 
							row.get('option_3')
						]
						
						# Correct answer index
						raw_correct_index = row.get('correct_answer')  # Changed from 'correct_index' to 'correct_answer'
						try:
							correct_index = int(raw_correct_index)
						except (ValueError, TypeError):
							raise ValueError(f"Row {row_index}: Correct answer '{raw_correct_index}' is not a valid number.")
						
						# Validate index range (must be 0, 1, 2, or 3)
						if correct_index < 0 or correct_index > 3:
							raise ValueError(f"Row {row_index}: Correct answer index {correct_index} is out of bounds (must be 0-3).")
						
						# Creating or referencing the context
						context_obj, created = Context.objects.get_or_create(
							context_id=int(context_id),
							uploader=request.user,
							defaults={
								'context': context_text,
								'context_title': context_title,
							}
						)
						
						# 3. Create Question
						question_obj = Question.objects.create(
							q_id=q_id,
							question=question_text,
							target_level=target_level,
							question_difficulty=question_difficulty,
							question_discrimination=question_discrimination,
							question_facility=question_facility,
							context=context_obj,
							uploader=request.user
						)
						
						# 4. Create Answers
						for index, opt_text in enumerate(options_data):
							# Skip if option string is missing/empty
							if not opt_text:
								continue
								
							is_correct_option = (index == correct_index)
							
							Answer.objects.create(
								question_linked=question_obj,
								answer=opt_text,
								is_correct=is_correct_option
							)
						
						count += 1
				
				messages.success(request, f"Successfully imported {count} MCQs.", extra_tags="success")
			
			except ValueError as ve:
				messages.error(request, f"Data Error: {str(ve)}", extra_tags="danger")
				return redirect('upload_csv')
			
			except Exception as e:
				messages.error(request, f"System Error: {str(e)}", extra_tags="danger")
				return redirect('upload_csv')
			
			return redirect('index')
			
	else:
		form = CSVuploadForm()

	template_name = "directory/upload_csv.html"
	context = {
		"form": form,
	}

	return render(request, template_name, context)
	
	
#def