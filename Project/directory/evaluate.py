# Libraries imports
import pandas as pd
import pickle

# Text2Props imports
from text2props.text2props.constants import QUESTION_DF_COLS, Q_ID, Q_TEXT, CORRECT_TEXTS, WRONG_TEXTS


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





def evaluate(questions_info, model_instance):
	
	
	# Preparing the data
	df_test = prepare_test_data(questions_info)
	
	
	# Loading the user-selected AI model from the pickle file
	with model_instance.pickle_file.open('rb') as f:
		text2props_model = pickle.load(f)
	#with
	
	# perform predictions
	predictions = text2props_model.predict(df_test)
	print(predictions) # To have a look at the individual predictions
	
	
#def 