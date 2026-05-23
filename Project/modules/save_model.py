# Libraries imports
import pickle
import io

# Django imports
from django.core.files.base import ContentFile
from directory.models import TrainedModel


# Saving the pickle file and creating an object in the DB to link it to a user
def save_model(text2props_model, object_info):
	
	# Create an in-memory byte stream
	buffer = io.BytesIO()
	
	# Pickle the model into the buffer
	pickle.dump(text2props_model, buffer)
	
	
	# Create the Django Model instance
	new_model_record = TrainedModel(
		title=object_info.title,
		public=object_info.public,
		uploader=object_info.uploader,
		parameter=object_info.parameter,
	)
	
	# Construct a unique filename using the UUID
	# We use the instance's pre-generated UUID for the filename
	filename = f"{new_model_record.id}.pkl"
	
	# Safely extracts the raw bytes directly from the memory buffer
	binary_data = buffer.getvalue()
	
	# Save the buffer content to the FileField
	new_model_record.pickle_file.save(filename, ContentFile(binary_data), save=True)
	
	# Clean up the buffer
	buffer.close()
	
#def 