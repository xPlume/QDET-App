
from text2props.example_model_1 import runner

# Function that prepares the data in the correct
# format before sending it to the ML model
def data_preparation(question, answers):
	
	"""
	for answer in answers:
		pivot = 0
		if (answer.is_correct == True):
			correct_answer_number = pivot
		#if
		pivot += 1
	#for
	
	
	new_row_dict = {
		'context_id': [question.context.context_id],
		'context_title': [question.context.context_title],
		'text': [question.context.context],
		'target_level': [question.target_level],
		'q_id': [question.q_id],  # Format: C{}_Q{}
		'question': [question.question],
		'correct_answer': [correct_answer_number], # int or string? Currently we send an int
		'question_difficulty': [question.question_difficulty],
		'question_discrimination': [question.question_discrimination],
		'question_facility': [question.question_facility],
		'option_0': [answers[0].answer],
		'option_1': [answers[1].answer],
		'option_2': [answers[2].answer],
		'option_3': [answers[3].answer],
	}
	"""
	
	# Call the ML model
	# ML_Result = [Name_of_the_ML_model_function](new_row_dict)
	
	# Save the result in the database
	
	
	# Running the model
	runner(question, answers)
	
#def