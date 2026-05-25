import pandas as pd
import math

from modules.utils import prediction_values
from directory.models import Statistic


# Converts "nan" pandas values to "None"
def convert_nan(val):
	
	if val is None:
		return None
	#if
	
	# Check if the value is a float NaN
	if isinstance(val, float) and math.isnan(val):
		return None
	#if
	
	return val
#def


"""
Calculates statistical metrics from a list of float values
using pandas for maximum efficiency.
"""
def statistical_metrics(model_used, user):
	
	# Obtaining the dataset
	float_data = prediction_values(model_used, user)
	
	
	# Return empty metrics if the list is empty to prevent runtime errors
	if not float_data:
		return {metric: None for metric in [
			"Mean", "Standard Error", "Median", "Mode", "Standard Deviation",
			"Sample Variance", "Kurtosis", "Skewness", "Range", "Minimum", "Maximum", "Count"
		]}
	#if not
	
	# Convert the list to a pandas Series
	series = pd.Series(float_data)
	
	# Mode can return multiple values if there's a tie; we take the first one.
	# If all values are unique, pandas returns all of them, so we handle that case.
	mode_series = series.mode()
	mode_value = mode_series.iloc[0] if not mode_series.empty else None
	
	
	# Calculating Range
	minimum = series.min()
	maximum = series.max()
	data_range = maximum - minimum
	
	
	# If entity of for that exact model and user exists, delete it.
	Statistic.objects.filter(user=user, model_used=model_used).delete()
	
	# Saving the results in a new object
	new_statistics_instance = Statistic(
		user = user,
		model_used = model_used,
		mean = convert_nan(series.mean()),
		std_error = convert_nan(series.sem()),
		median = convert_nan(series.median()),
		mode = convert_nan(mode_value),
		std_deviation = convert_nan(series.std()),
		variance = convert_nan(series.var()),
		kurtosis = convert_nan(series.kurt()),
		skewness = convert_nan(series.skew()),
		minimum = convert_nan(minimum),
		maximum = convert_nan(maximum),
		range = convert_nan(data_range),
		count = int(series.count()),
	)
	
	new_statistics_instance.save()
	
#def 