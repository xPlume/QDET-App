from directory.models import Prediction


""" 
Function that queries the values of a set of
predictions, and converts the values to floats
"""
def prediction_values(model_used, user):
	
	# Querying the prediction values
	decimal_values = Prediction.objects.filter(
		user=user,
		model_used=model_used
	).values_list('value', flat=True)
	
	
	# Converting the database values into floats
	float_data = [float(val) for val in decimal_values if val is not None]
	
	if not float_data:
		return None
	#if not
	
	return float_data
	
#def