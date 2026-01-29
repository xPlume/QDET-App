import csv
import io
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import transaction
from django.contrib.auth.decorators import login_required

from directory.forms import CSVuploadForm
from directory.models import Question, Answer


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
            
            # Skip header if necessary
            next(reader, None)

            try:
                with transaction.atomic():
                    count = 0
                    for row_index, row in enumerate(reader):
                        # 1. Basic Validation
                        if len(row) < 10:
                            # You might want to log this or skip silently
                            continue

                        # 2. Extract Data
                        context_id = row[0]
                        context_text = row[1]
                        q_id = row[2]
                        question_text = row[3]
                        target_level = row[4]
                        
                        # Options are columns 5, 6, 7, 8
                        options_data = [row[5], row[6], row[7], row[8]]
                        
                        # Correct answer index is column 9 (e.g., "0", "2")
                        try:
                            correct_index = int(row[9])
                        except ValueError:
                            raise ValueError(f"Row {row_index + 1}: Correct answer '{row[9]}' is not a number.")

                        # Validate index range (must be 0, 1, 2, or 3)
                        if correct_index < 0 or correct_index > 3:
                            raise ValueError(f"Row {row_index + 1}: Correct answer index {correct_index} is out of bounds (must be 0-3).")

                        # 3. Create Question
                        question_obj = Question.objects.create(
                            context_id=int(context_id),
                            context=context_text,
                            q_id=q_id,
                            question=question_text,
                            target_level=target_level,
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
                        
                        count += 1

                messages.success(request, f"Successfully imported {count} questions.", extra_tags="success")

            except ValueError as ve:
                messages.error(request, f"Data Error: {str(ve)}", extra_tags="danger")
                return redirect('upload_csv')
            except Exception as e:
                messages.error(request, f"System Error: {str(e)}", extra_tags="danger")
                return redirect('upload_csv')
            
            return redirect('index')
    else:
        form = CSVuploadForm()

    return render(request, "directory/upload_csv.html", {'form': form})