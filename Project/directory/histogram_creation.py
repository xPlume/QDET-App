import io
import matplotlib
matplotlib.use('Agg')  # Prevents GUI windows from spinning up on your server
import matplotlib.pyplot as plt
from django.core.files.base import ContentFile
from directory.models import Histogram, Prediction



def create_histogram(model_used, user):
	
	
	# 1. Query only the 'value' column from the database
	decimal_values = Prediction.objects.filter(
		user=user,
		model_used=model_used
	).values_list('value', flat=True)
	
	model_title = f"[{model_used.parameter.replace(' ', '_')}] {model_used.title.replace(' ', '_')}"
	
	# 2. Adapt the line to convert those database values into floats
	float_data = [float(val) for val in decimal_values if val is not None]
	
	
	
	if not float_data:
		return None
	#if not
	
	
	
	# 2. Generate the plot
	plt.figure(figsize=(8, 5))
	plt.hist(float_data, bins='auto', edgecolor='black', alpha=0.7)
	plt.title(model_title)
	plt.xlabel('Values')
	plt.ylabel('Frequency')
	plt.grid(axis='y', alpha=0.75)
	
	# 3. Save the plot to an in-memory bytes buffer
	buffer = io.BytesIO()
	plt.savefig(buffer, format='png', bbox_inches='tight')
	buffer.seek(0)
	plt.close()  # Clean up memory allocation
	
	# 4. Construct a Django file object and save the model instances
	chart_instance = Histogram(
		user = user,
		model_used = model_used,
	)
	
	# Wrap the buffer contents into a Django content file 
	filename = f"histogram_{model_title}.png"
	chart_instance.chart_image.save(filename, ContentFile(buffer.getvalue()), save=True)
	
	return chart_instance
#def