from text2props.text2props.model import Text2PropsModel
from text2props.text2props.modules.latent_traits_calibration import KnownParametersCalibrator
from text2props.text2props.modules.estimators_from_text import MajorityEstimatorFromText

from text2props.text2props.constants import DATA_PATH, WRONGNESS, QUESTION_DF_COLS, Q_ID, Q_TEXT, CORRECT_TEXTS, WRONG_TEXTS
import os
import pandas as pd
import random

from tabulate import tabulate


def data_preparation(question, answers):
	# 1. Calculate Wrongness
	WRONGNESS = 'wrongness' # Assuming this is your constant name
	wrongness_dictionary = {
		WRONGNESS: {
			question.q_id: 1 - question.question_facility
		}
	}
	
	
	pivot = 0
	for answer in answers:
		if (answer.is_correct == True):
			correct_answer_number = pivot
		#if
		pivot += 1
	#for
	
	
	# 2. Prepare the Question DataFrame (single-row DF)
	# Map your object attributes to the required constants

	# Logic for correct/wrong texts
	options = [answers[0].answer, answers[1].answer, answers[2].answer, answers[3].answer]
	correct_texts = [options[correct_answer_number]]
	wrong_texts = [text for idx, text in enumerate(options) if idx != correct_answer_number]

	data = {
		Q_ID: [question.q_id],
		Q_TEXT: [f"Context:\n{question.context.context}\n\nQuestion:\n{question.question}"],
		CORRECT_TEXTS: [correct_texts],
		WRONG_TEXTS: [wrong_texts]
	}

	# Create the DataFrame for this single question
	output_df = pd.DataFrame(data, columns=QUESTION_DF_COLS)

	# 3. Train/Test Split Logic
	# Since you are processing ONE question at a time, we decide if it belongs to train or test.
	# If you need to simulate a split, we can use a simple random check.
	"""
	if random.random() < 0.8:
		train_df = output_df
		test_df = pd.DataFrame(columns=QUESTION_DF_COLS)
	else:
		train_df = pd.DataFrame(columns=QUESTION_DF_COLS)
		test_df = output_df
	"""
	
	# Since we have only ONE question here, it goes into the test
	train_df = pd.DataFrame(columns=QUESTION_DF_COLS)
	test_df = output_df

	return wrongness_dictionary, train_df, test_df


def runner(question, answers):
	
	
	known_latent_traits, df_train, df_test = data_preparation(question, answers)
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
	known_latent_traits, df_train, df_test = data_preparation(question, answers)

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

