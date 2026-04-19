# Libraries imports
import pandas as pd
import pickle
import io

# Text2Props imports
from text2props.text2props.model import Text2PropsModel
from text2props.text2props.modules.latent_traits_calibration import KnownParametersCalibrator
from text2props.text2props.modules.estimators_from_text import MajorityEstimatorFromText
from text2props.text2props.constants import DATA_PATH, WRONGNESS, QUESTION_DF_COLS, Q_ID, Q_TEXT, CORRECT_TEXTS, WRONG_TEXTS

# Django imports
from django.core.files.base import ContentFile
from directory.models import TrainedModel




# Taking all the questions, setting the proper format, and sending them all into the Training.
def data_preparation(questions_queryset):
    
	
	# 1. Convert QuerySet to a list to allow shuffling and easy indexing
	questions_list = list(questions_queryset)
	#print(f"[INFO] Length of the original dataset: {len(questions_list)}")
	
	# 2. Build the wrongness dictionary
	# Note: WORKS FOR QUESTION_FACILITY ONLY
	wrongness_dictionary = {
		WRONGNESS: {
			q.id: 1 - float(q.question_facility)
			for q in questions_list
		}
	}
	#print(f"[INFO] Number of questions in the wrongness dictionary: {len(wrongness_dictionary[WRONGNESS])}")
	
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
		#for
		
		return pd.DataFrame(data, columns=QUESTION_DF_COLS)
	#def
	
	
	# 3. Process all questions into the training set
	# We no longer split by context_id; we pass the entire questions_list
	train_df = prepare_questions_list(questions_list)

	# Returning None or an empty DataFrame for the third value to avoid breaking 
	# unpacking logic if the calling code expects three returns.
	return wrongness_dictionary, train_df
	
# def





# Saving the pickle file and creating an object in the DB to link it to a user
def save_trained_model_to_db(text2props_model, object_info):
	# 1. Create an in-memory byte stream
	buffer = io.BytesIO()

	# 2. Pickle the model into the buffer
	pickle.dump(text2props_model, buffer)

	# 3. Seek to the start of the buffer so Django can read it
	buffer.seek(0)

	# 4. Create the Django Model instance
	new_model_record = TrainedModel(
		title=object_info.title,
		public=object_info.public,
		uploader=object_info.uploader,
	)
	
	# 5. Construct a unique filename using the UUID
	# We use the instance's pre-generated UUID for the filename
	filename = f"{new_model_record.id}.pkl"
	
	# 6. Save the buffer content to the FileField
	new_model_record.pickle_file.save(filename, ContentFile(buffer.read()), save=True)
	
	return new_model_record
#def 




def train_model(questions_info, object_info):
	
	# Preparing the data
	# All questions are send as Training
	known_latent_traits, df_train = data_preparation(questions_info)
	
	
	# Define the "calibrator".
	#   This is the object that looks at the students responses and measures the "true" values for the latent traits.
	#   In this case, we already know the latent traits (available in the dataset).
	latent_traits_calibrator = KnownParametersCalibrator(latent_traits=known_latent_traits)
	
	
	# Picking the AI module we want to train
	estimator_from_text = MajorityEstimatorFromText()
	
	# The text2props model is made of a latent_traits_calibrator + estimator_from_text pair.
	text2props_model = Text2PropsModel(latent_traits_calibrator, estimator_from_text)

	# Train the text2props_model
	text2props_model.train(df_train=df_train)
	
	
	# Saving the tained model as a pickle file, with an object in the DB
	new_model_record = save_trained_model_to_db(text2props_model, object_info)
	
	
#def 