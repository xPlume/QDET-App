# Libraries imports
import pandas as pd
import pickle
import io
import random
from sklearn.ensemble import RandomForestRegressor

# Text2Props imports
from text2props.text2props.model import Text2PropsModel
from text2props.text2props.modules.latent_traits_calibration import KnownParametersCalibrator
#from text2props.text2props.modules.estimators_from_text import MajorityEstimatorFromText

from text2props.text2props.modules.estimators_from_text import (
    FeatureEngAndRegressionPipeline,
    FeatureEngAndRegressionEstimatorFromText,
)
from text2props.text2props.modules.feature_engineering import FeatureEngineeringModule
from text2props.text2props.modules.feature_engineering.components import LinguisticFeaturesComponent, ReadabilityFeaturesComponent
from text2props.text2props.modules.regression import RegressionModule
from text2props.text2props.modules.regression.components import SklearnRegressionComponent


from text2props.text2props.constants import QUESTION_DF_COLS, Q_ID, Q_TEXT, CORRECT_TEXTS, WRONG_TEXTS, DIFFICULTY, DISCRIMINATION, FACILITY

# Django imports
from django.core.files.base import ContentFile
from directory.models import TrainedModel
from django.db.models import Max, Min




def data_preparation(questions_info, parameter):
    
	
	# Parameters: 
	# 1: Question Difficulty
	# 2: Question Discrimination
	# 3: Question Facility
	
	# Create the wrongness dictionary
	if parameter== '1': # Difficulty
		wrongness_dictionary = {
			DIFFICULTY: {
				q.id: 1 - float(q.question_difficulty)
				for q in questions_info
			}
		}
	elif parameter== '2': # Discrimination
		wrongness_dictionary = {
			DISCRIMINATION: {
				q.id: 1 - float(q.question_discrimination)
				for q in questions_info
			}
		}
	elif parameter== '3': # Facility
		wrongness_dictionary = {
			FACILITY: {
				q.id: 1 - float(q.question_facility)
				for q in questions_info
			}
		}
	#if
	
	
	def prepare_questions_list(qs):
		# Helper to map QuerySet objects to the required DataFrame format 
		data = []
		for q in qs:
			# Get all answers for this question
			all_answers = list(q.answers.all())
			correct_texts = [a.answer for a in all_answers if a.is_correct]
			wrong_texts = [a.answer for a in all_answers if not a.is_correct]
			
			data.append({
				Q_ID: q.id,
				Q_TEXT: f"Context:\n{q.context.context}\n\nQuestion:\n{q.question}",
				CORRECT_TEXTS: correct_texts,
				WRONG_TEXTS: wrong_texts,
				'context_id': q.context.id
			})
		#for
		
		return pd.DataFrame(data)
	#def
	
	
	# Train/Test Split logic based on Context ID
	# We extract unique context IDs from the QuerySet
	all_context_ids = list(set(q.context.id for q in questions_info))
	random.shuffle(all_context_ids)
	
	n_train = int(len(all_context_ids) * 0.8)
	train_context_ids = set(all_context_ids[:n_train])
	
	# Split the original QuerySet/list into two groups
	train_qs = [q for q in questions_info if q.context.id in train_context_ids]
	test_qs = [q for q in questions_info if q.context.id not in train_context_ids]
	
	"""
	print(f"[INFO] Number training contexts: {n_train}")
	print(f"[INFO] Length (n questions) of train_df: {len(train_qs)}")
	print(f"[INFO] Length (n questions) of test_df: {len(test_qs)}")
	"""
	
	# Convert to DataFrames
	train_df = prepare_questions_list(train_qs)
	test_df = prepare_questions_list(test_qs)
	
	# Cleanup: Remove the temporary context_id column used for splitting if not in QUESTION_DF_COLS
	train_df = train_df[QUESTION_DF_COLS]
	test_df = test_df[QUESTION_DF_COLS]
	
	return wrongness_dictionary, train_df, test_df
#def




# Obtain the max and min values of the latent-trait
def get_range(questions_info, parameter):
	
	# Parameters: 
	# 1: Question Difficulty
	# 2: Question Discrimination
	# 3: Question Facility
	
	# Aggregate min and max directly from the database
	if parameter== '1': # Difficulty
		result = questions_info.aggregate(
			min_diff=Min('question_difficulty'),
			max_diff=Max('question_difficulty')
		)
	elif parameter== '2': # Discrimination
		result = questions_info.aggregate(
			min_diff=Min('question_discrimination'),
			max_diff=Max('question_discrimination')
		)
	elif parameter== '3': # Facility
		result = questions_info.aggregate(
			min_diff=Min('question_facility'),
			max_diff=Max('question_facility')
		)
	#elif
	
	# Cast to float in case the database field is a Decimal or string
	min_val = float(result['min_diff']) if result['min_diff'] is not None else 0.0
	max_val = float(result['max_diff']) if result['max_diff'] is not None else 0.0
	
	return min_val, max_val
#def





# Saving the pickle file and creating an object in the DB to link it to a user
def save_trained_model_to_db(text2props_model, object_info):
	# Create an in-memory byte stream
	buffer = io.BytesIO()

	# Pickle the model into the buffer
	pickle.dump(text2props_model, buffer)

	# Seek to the start of the buffer so Django can read it
	buffer.seek(0)

	# Create the Django Model instance
	new_model_record = TrainedModel(
		title=object_info.title,
		public=object_info.public,
		uploader=object_info.uploader,
	)
	
	# Construct a unique filename using the UUID
	# We use the instance's pre-generated UUID for the filename
	filename = f"{new_model_record.id}.pkl"
	
	# Save the buffer content to the FileField
	new_model_record.pickle_file.save(filename, ContentFile(buffer.read()), save=True)
	
#def 




def train_model(questions_info, parameter):
	
	# Preparing the data
	# All questions are send as Training
	#known_latent_traits, df_train = data_preparation(questions_info, parameter)
	known_latent_traits, df_train, df_test = data_preparation(questions_info, parameter)
	
	
	# Define the "calibrator".
	#   This is the object that looks at the students responses and measures the "true" values for the latent traits.
	#   In this case, we already know the latent traits (available in the dataset).
	latent_traits_calibrator = KnownParametersCalibrator(latent_traits=known_latent_traits)
	
	
	# Obtaining max and min values of the latent-trait
	min_val, max_val = get_range(questions_info, parameter)
	
	
	# Picking the AI module we want to train based on the parameter
	
	# Parameters: 
	# 1: Question Difficulty
	# 2: Question Discrimination
	# 3: Question Facility
	
	# Create the wrongness dictionary
	if parameter== '1': # Difficulty
		estimator_from_text = FeatureEngAndRegressionEstimatorFromText(
			{
				DIFFICULTY: FeatureEngAndRegressionPipeline(
					FeatureEngineeringModule([ReadabilityFeaturesComponent(), LinguisticFeaturesComponent()]),
					RegressionModule([SklearnRegressionComponent(RandomForestRegressor(random_state=42), latent_trait_range=(min_val, max_val))])
				)
			}
		)
	elif parameter== '2': # Discrimination
		estimator_from_text = FeatureEngAndRegressionEstimatorFromText(
			{
				DISCRIMINATION: FeatureEngAndRegressionPipeline(
					FeatureEngineeringModule([ReadabilityFeaturesComponent(), LinguisticFeaturesComponent()]),
					RegressionModule([SklearnRegressionComponent(RandomForestRegressor(random_state=42), latent_trait_range=(min_val, max_val))])
				)
			}
		)
	elif parameter== '3': # Facility
		estimator_from_text = FeatureEngAndRegressionEstimatorFromText(
			{
				FACILITY: FeatureEngAndRegressionPipeline(
					FeatureEngineeringModule([ReadabilityFeaturesComponent(), LinguisticFeaturesComponent()]),
					RegressionModule([SklearnRegressionComponent(RandomForestRegressor(random_state=42), latent_trait_range=(min_val, max_val))])
				)
			}
		)
	#if
	
	
	
	# The text2props model is made of a latent_traits_calibrator + estimator_from_text pair.
	text2props_model = Text2PropsModel(latent_traits_calibrator, estimator_from_text)

	# Train the text2props_model
	text2props_model.train(df_train=df_train)
	
	
	# Saving the tained model as a pickle file, with an object in the DB
	#new_model_record = save_trained_model_to_db(text2props_model, object_info)
	
	
	# perform predictions
	predictions = text2props_model.predict(df_test)
	#print(predictions)  # To have a look at the individual predictions
	
	
	# evaluate model 
	results = text2props_model.compute_error_metrics_latent_traits_estimation(df_test)
	#print(results)
	
	return results, text2props_model
	
	
#def 