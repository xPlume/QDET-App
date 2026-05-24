import pandas as pd

from modules.utils import prediction_values
from directory.models import Statistic


"""
Calculates statistical metrics from a list of float values
using pandas for maximum efficiency.
"""
def statistical_metrics(model_used, user):
	
	# Obtaining the dataset for the histogram
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
	range = maximum - minimum
	
	
	# Saving the results in a new object
	new_statisctics_instance = Statistic(
		user = user,
		model_used = model_used,
		mean = series.mean(),
		std_error = series.sem(),
		median = series.median(),
		mode = mode_value,
		std_deviation = series.std(),
		variance = series.var(),
		kurtosis = series.kurt(),
		skewness = series.skew(),
		minimum = minimum,
		maximum = maximum,
		range = range,
		count = int(series.count()),
	)
	
	new_statisctics_instance.save()
	
#def 