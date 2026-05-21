import io
import matplotlib.pyplot as plt
import seaborn as sns
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
	label_mapping = {
		"difficulty": "Difficulty (%)",
		"discrimination": "Discrimination",
		"facility": "Facility"
	}
	x_label = label_mapping.get(parameter_value, "Values")
	
	color_mapping = {
		"difficulty": "dodgerblue",
		"discrimination": "orange",
		"facility": "limegreen",
	}
	
	title_mapping = {
		"difficulty": "Difficulty",
		"discrimination": "Discrimination",
		"facility": "Facility"
	}
	
	# Plotting the histogram
	sns.histplot(
		data=float_data, 
		bins='auto', 
		color=color_mapping.get(parameter_value),        
		alpha=0.7,             
		edgecolor="white",      
		linewidth=0.8,
		kde=True,              
		label=title_mapping.get(parameter_value),
		ax=ax
	)
	
	# Labels & Typography
	ax.set_ylabel('Frequency', fontsize=11, labelpad=10, color='#34495e')
	ax.set_xlabel(x_label, fontsize=11, labelpad=10, color='#34495e')

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