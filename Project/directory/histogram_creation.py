import io
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from django.core.files.base import ContentFile
from directory.models import Histogram, Prediction



def create_histogram(model_used, user):
	
	# Obtaining the parameter
	parameter_value = model_used.parameter
	
	# Querying the prediction values
	decimal_values = Prediction.objects.filter(
		user=user,
		model_used=model_used
	).values_list('value', flat=True)
	
	model_title = f"[{model_used.parameter.replace(' ', '_')}] {model_used.title.replace(' ', '_')}"
	
	# Converting the database values into floats
	float_data = [float(val) for val in decimal_values if val is not None]
	
	if not float_data:
		return None
	#if not
	
	
	
	# Generating the graph
	
	
	sns.set_theme(style="whitegrid", context="notebook")
	fig, ax = plt.subplots(figsize=(8, 5))
	
	# Calculating the total number of elements
	total_elements = len(float_data)
	
	# Map dynamic X-axis labels to provide context for the legend label
	metric_configs = {
		"difficulty": {
			"x_label": "Difficulty (%)",
			"legend_title": "Difficulty",
			"color": "dodgerblue",
			"axis_range": (0, 100, 10)  # From 0% to 100% every 10%
		},
		"discrimination": {
			"x_label": "Discrimination",
			"legend_title": "Discrimination",
			"color": "orange",
			"axis_range": (-1.0, 1.0, 0.2)  # E.g., -1.0 to 1.0 every 0.2
		},
		"facility": {
			"x_label": "Facility",
			"legend_title": "Facility",
			"color": "limegreen",
			"axis_range": (0.0, 1.0, 0.1)  # From 0.0 to 1.0 every 0.1
		}
	}
	
	# Fallback configuration if parameter doesn't match keys
	config = metric_configs.get(parameter_value.lower(), {
		"x_label": "Values",
		"legend_title": "Distribution",
		"color": "dodgerblue",
		"axis_range": (min(float_data), max(float_data), (max(float_data) - min(float_data)) / 5)
	})
	
	# Plotting the histogram
	sns.histplot(
		data=float_data, 
		bins='auto', 
		color=config["color"],        
		alpha=0.7,             
		edgecolor="white",      
		linewidth=0.8,
		kde=True,              
		label=config["legend_title"],
		ax=ax
	)
	
	# Applying fixed x-axis intervals
	start, stop, step = config["axis_range"]
	fixed_ticks = np.arange(start, stop + (step / 100), step) 
	
	ax.set_xticks(fixed_ticks)
	ax.set_xlim(start, stop)
	
	
	# Labels & Typography
	ax.set_ylabel('Frequency', fontsize=11, labelpad=10, color='#34495e')
	ax.set_xlabel(config["x_label"], fontsize=11, labelpad=10, color='#34495e')
	
	# Legend
	ax.legend(loc="upper left", frameon=True, facecolor="white", edgecolor="none")

	# N Count Badge (N = ...)
	text_str = f"N = {total_elements:,}"
	ax.text(
		0.95, 0.95, text_str, 
		transform=ax.transAxes, 
		fontsize=10,
		weight='semibold',
		color='#566573',
		ha='right', va='top',
		bbox=dict(boxstyle='round,pad=0.5', facecolor='#f8f9f9', edgecolor='#e5e7e9', alpha=0.85)
	)
	
	# Removing graph borders
	sns.despine(left=True, bottom=False)
	
	# Displaying only horizontal lines
	ax.xaxis.grid(False) 
	ax.yaxis.grid(True, linestyle='-', alpha=0.4, color='#e0e0e0') 
	
	# Saving
	buffer = io.BytesIO()
	plt.savefig(buffer, format='png', bbox_inches='tight', dpi=150)
	buffer.seek(0)
	plt.close(fig)
	
	
	# If entity of that exact histogram exists, delete it.
	Histogram.objects.filter(user=user, model_used=model_used).delete()
	
	# Saving a Histogram object in the database
	chart_instance = Histogram(
		user = user,
		model_used = model_used,
	)
	
	# Saving the histogram as an image
	filename = f"histogram_{model_title}.png"
	chart_instance.chart_image.save(filename, ContentFile(buffer.getvalue()), save=True)
	
	return chart_instance
#def