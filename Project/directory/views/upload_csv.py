import csv
import io
from decimal import Decimal, InvalidOperation
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import transaction
from django.contrib.auth.decorators import login_required

from directory.forms import CSVuploadForm
from directory.models import Context, Question, Answer
from directory.utils import safe_decimal


@login_required
def upload_csv(request):
	if request.method == 'POST':
		form = CSVuploadForm(request.POST, request.FILES)
		if form.is_valid():
			csv_file = request.FILES['file']
			
			# Use utf-8-sig to handle potential BOM from Excel
			decoded_file = csv_file.read().decode('utf-8-sig')
			io_string = io.StringIO(decoded_file)
			reader = csv.reader(io_string, delimiter=',')
			
			# Skip header if exists
			next(reader, None)
			
			try:
				with transaction.atomic():
					count = 0
					for row_index, row in enumerate(reader):
						# 1. Basic Validation
						if len(row) < 10:
							# You might want to log this or skip silently
							continue
						#if
						
						# 2. Extract Data
						context_id = row[0]
						context_title = row[1]
						context_text = row[2]
						target_level = row[3]
						q_id = row[4]
						question_text = row[5]
						question_difficulty = safe_decimal(row[7], places=2)
						question_discrimination = safe_decimal(row[8], places=3)
						question_facility = safe_decimal(row[9], places=3)
						
						# Options are columns 5, 6, 7, 8
						options_data = [row[10], row[11], row[12], row[13]]
						
						# Correct answer index is column 9 (e.g., "0", "2")
						try:
							correct_index = int(row[6])
						except ValueError:
							raise ValueError(f"Row {row_index + 1}: Correct answer '{row[6]}' is not a number.")
						#except
						
						# Validate index range (must be 0, 1, 2, or 3)
						if correct_index < 0 or correct_index > 3:
							raise ValueError(f"Row {row_index + 1}: Correct answer index {correct_index} is out of bounds (must be 0-3).")
						#if
						
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
							context = context_obj,
							uploader=request.user
						)
						
						# 4. Create Answers
						# We use enumerate to get the current index (0, 1, 2, 3)
						for index, opt_text in enumerate(options_data):
							
							# Logic: If the current loop index matches the CSV integer
							is_correct_option = (index == correct_index)
							
							Answer.objects.create(
								question_linked=question_obj,
								answer=opt_text,
								is_correct=is_correct_option
							)
						#for
						
						count += 1
					#for
				
				#with
				messages.success(request, f"Successfully imported {count} MCQs.", extra_tags="success")
			#try
			
			except ValueError as ve:
				messages.error(request, f"Data Error: {str(ve)}", extra_tags="danger")
				return redirect('upload_csv')
			#except 
			
			except Exception as e:
				messages.error(request, f"System Error: {str(e)}", extra_tags="danger")
				return redirect('upload_csv')
			#except
			
			return redirect('index')
		#if
	#if
	
	else:
		form = CSVuploadForm()
	#else
	
	
	
	template_name = "directory/upload_csv.html"
	context = {
		"form": form,
	}
	
	return render(request, template_name, context)
	
	
#def