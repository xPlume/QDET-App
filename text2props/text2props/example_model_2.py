from text2props.text2props.model import Text2PropsModel
from text2props.text2props.modules.latent_traits_calibration import KnownParametersCalibrator
from text2props.text2props.modules.estimators_from_text import MajorityEstimatorFromText

from text2props.text2props.constants import DATA_PATH, WRONGNESS, QUESTION_DF_COLS, Q_ID, Q_TEXT, CORRECT_TEXTS, WRONG_TEXTS
import os
import pandas as pd
import random

from tabulate import tabulate


def data_preparation(questions_queryset):
    
	
    # 1. Convert QuerySet to a list to allow shuffling and easy indexing
    questions_list = list(questions_queryset)
    print(f"[INFO] Length of the original dataset: {len(questions_list)}")

    # 2. Build the wrongness dictionary
    # Note: WORKS FOR QUESTION_FACILITY ONLY
    wrongness_dictionary = {
        WRONGNESS: {
            q.id: 1 - float(q.question_facility)
            for q in questions_list
        }
    }
    print(f"[INFO] Number of questions in the wrongness dictionary: {len(wrongness_dictionary[WRONGNESS])}")

    def prepare_questions_list(qs_subset):
        """ Maps Django objects to the format needed by text2props. """
        data = []
        for q in qs_subset:
            # Get all answers for this question (cached by prefetch)
            all_answers = list(q.answers.all())
            
            correct_texts = [a.answer for a in all_answers if a.is_correct]
            wrong_texts = [a.answer for a in all_answers if not a.is_correct]

            data.append({
                Q_ID: q.id,
                # Accessing q.context.text (cached by select_related)
                Q_TEXT: f"Context:\n{q.context.context}\n\nQuestion:\n{q.question}",
                CORRECT_TEXTS: correct_texts,
                WRONG_TEXTS: wrong_texts
            })
        
        return pd.DataFrame(data, columns=QUESTION_DF_COLS)

    # 3. Train/test split based on Context ID
    # We group by context_id to ensure a passage doesn't leak from train to test
    context_ids = list(set(q.context_id for q in questions_list))
    random.shuffle(context_ids)
    
    n_train = int(len(context_ids) * 0.8)
    train_context_ids = set(context_ids[:n_train])

    train_subset = [q for q in questions_list if q.context_id in train_context_ids]
    test_subset = [q for q in questions_list if q.context_id not in train_context_ids]

    print(f"[INFO] Number training contexts: {n_train}")
    print(f"[INFO] Length (n questions) of train_df: {len(train_subset)}")
    print(f"[INFO] Length (n questions) of test_df: {len(test_subset)}")

    # 4. Convert to DataFrames
    train_df = prepare_questions_list(train_subset)
    test_df = prepare_questions_list(test_subset)

    return wrongness_dictionary, train_df, test_df


def runner(questions_info):
	
	
	known_latent_traits, df_train, df_test = data_preparation(questions_info)
	
	"""
	print("")
	print("")
	print("")
	print("")
	print("WRONGNESS_DICTIONARY")
	print(known_latent_traits)
	print("")
	print("")
	print("")
	
	# 1. Don't truncate column width (allows full text to show)
	pd.set_option('display.max_colwidth', None)

	# 2. Show all columns (don't use '...' in the middle of columns)
	pd.set_option('display.max_columns', None)
	
	# 3. Show all rows (don't use '...' in the middle of the dataset)
	pd.set_option('display.max_rows', None)
	
	# 4. Don't wrap the table to the next line (prevents breaking the table)
	pd.set_option('display.expand_frame_repr', False)
	
	print("--- TRAIN_DF CONTENT ---")
	print(df_train)
	#print(tabulate(df_train, headers='keys', tablefmt='grid'))
	
	print("")
	print("")
	print("")
	
	print("\n--- TEST_DF CONTENT ---")
	print(df_test)
	"""
	# Prepare data. This is custom for the given .csv()
	known_latent_traits, df_train, df_test = data_preparation(questions_info)

	# Define the "calibrator".
	#   This is the object that looks at the students responses and measures the "true" values for the latent traits.
	#   In this case, we already know the latent traits (available in the dataset).
	latent_traits_calibrator = KnownParametersCalibrator(latent_traits=known_latent_traits)
	# This would be needed to calibrate the latent traits using the responses of students.
	# latent_traits_calibrator = WrongnessCalibrator(df_gte)

	# Define the "Estimator from text".
	#   This is the Machine Learning model that receives the text and predicts the latent trait.
	#   In this case, a toy model (always predicts the average value of the latent trait, regardless of the text).
	estimator_from_text = MajorityEstimatorFromText()

	# The text2props model is made of a latent_traits_calibrator + estimator_from_text pair.
	text2props_model = Text2PropsModel(latent_traits_calibrator, estimator_from_text)

	# Train the text2props_model
	text2props_model.train(df_train=df_train)

	# perform predictions
	predictions = text2props_model.predict(df_test)
	# print(predictions)  # To have a look at the individual predictions

	# evaluate model and print results
	results = text2props_model.compute_error_metrics_latent_traits_estimation(df_test)
	print(results)
	


# --- --- COLUMN REQUIREMENTS and DATA FORMAT --- ---

# --- For the known_latent_traits dictionary ---
# It is a nested dictionary. First key is the name of the latent trait (one of WRONGNESS, DIFFICULTY, DISCRIMINATION)
# The values are dictionaries (the keys are the question IDs, the values the latent traits).
# Note: wrongness = 1 - facility

# --- for df_train and df_test ---
# These are the dataframes which contain the text of the questions and the value of the latent trait.
# Needs colums QUESTION_DF_COLS = [Q_ID, Q_TEXT, CORRECT_TEXTS, WRONG_TEXTS] (from text2props.constants)

# --- For df_gte ---
# This is the dataset that contains the responses of individual students to the questions (not needed here).
# Needs columns ANSWERS_DF_COLS (from text2props.constants)

