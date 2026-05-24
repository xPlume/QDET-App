# Libraries imports
import pandas as pd
import pickle

# Text2Props imports
from text2props.text2props.constants import QUESTION_DF_COLS, Q_ID, Q_TEXT, CORRECT_TEXTS, WRONG_TEXTS

# Django imports
from django.db import transaction
from django.contrib.auth import get_user_model
from django.db.models import Q

# Reference to other files
from directory.models import Prediction, Question


# Taking all the questions, and setting the proper format for the Test 
def prepare_test_data(questions_info):
    
    data = []
    for q in questions_info:
        # Get all answers for this question
        all_answers = list(q.answers.all())
        correct_texts = [a.answer for a in all_answers if a.is_correct]
        wrong_texts = [a.answer for a in all_answers if not a.is_correct]
        
        data.append({
            Q_ID: q.id,
            Q_TEXT: f"Context:\n{q.context.context}\n\nQuestion:\n{q.question}",
            CORRECT_TEXTS: correct_texts,
            WRONG_TEXTS: wrong_texts,
        })
        
    # Convert directly to DataFrame and filter by your specific columns
    test_df = pd.DataFrame(data)
    test_df = test_df[QUESTION_DF_COLS]
    
    return test_df
#def



"""
Function that takes the questions with their predictions.
If the question already had a prediction with the same model, delete it
then, save the new prediction. Else, just save the prediction.
"""
def save_predictions(questions_info, model_instance, prediction_result, user):
	
	# Obtaining the parameter
	parameter_value = model_instance.parameter 
	
	# Extracting the values of the predictions
	values_array = prediction_result.get(parameter_value)
	
	if values_array is None:
		raise ValueError(f"No evaluation values found for parameter: '{parameter_value}'")
	#if
	
	# Converting the Django queryset to a list
	questions_list = list(questions_info)
	
	# Safety Check: Ensure the lengths match before processing
	if len(questions_list) != len(values_array):
		raise ValueError(
			f"Mismatch length: Found {len(questions_list)} questions but {len(values_array)} values."
		)
	#if
	
	
	# Building the list of unsaved Prediction instances
	predictions_to_create = []
	
	for question, value in zip(questions_list, values_array):
		predictions_to_create.append(
			Prediction(
				question=question,
				model_used=model_instance,
				value=value,
				parameter=parameter_value,
				user=user,
			)
		)
	#for
	
	# Wrap the delete and insert in a single transaction to ensure data integrity
	with transaction.atomic():
		# Efficiently delete existing records matching the unique criteria
		# Because 'model_used' and 'user' are constant for this entire batch,
		# we only need to filter 'question' by the incoming list of questions.
		Prediction.objects.filter(
			model_used=model_instance,
			user=user,
			question__in=questions_list
		).delete()
		
		# Perform the single batch insert into the database
		created_predictions = Prediction.objects.bulk_create(predictions_to_create)
	#with
	
#def





def evaluate(questions_info, model_instance, user):
	
	
	# Preparing the data
	df_test = prepare_test_data(questions_info)
	
	
	# Loading the user-selected AI model from the pickle file
	with model_instance.pickle_file.open('rb') as f:
		text2props_model = pickle.load(f)
	#with
	
	# perform predictions
	predictions = text2props_model.predict(df_test)
	#print(predictions) # To have a look at the individual predictions
	
	
	# Saving predictions in the db
	save_predictions(questions_info, model_instance, predictions, user)
	
#def 