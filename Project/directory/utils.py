from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

from django.db import models

"""
Class used to centralised the TextChoices on all models
that save the latent-trait as an attribute:
models/TrainedModels.py; models/Preductions.py
"""
class ParameterChoices(models.TextChoices):
	
	# NAME = 'database_value', 'human-readable_label'
	DIFFICULTY = 'difficulty', 'Difficulty'
	DISCRIMINATION = 'discrimination', 'Discrimination'
	FACILITY = 'facility', 'Facility'
	
#class



# Function used in the views/upload_csv.py file
def safe_decimal(value, places=2):
	if value is None:
		return None
	#if
	
	# Clean the string (remove spaces, keep the minus sign!)
	clean_val = str(value).strip()
	
	# Handle Empty Fields
	# If the CSV cell is empty, return None (which becomes NULL in the DB)
	if not clean_val or clean_val.lower() in ['nan', 'none', '-']:
		return None
	#if not
	
	try:
		# Convert to Decimal
		number = Decimal(clean_val)
		
		# Optional: Force the correct decimal places to avoid rounding errors
		# This ensures -9.68234 becomes -9.68
		exponent = Decimal(10) ** -places
		return number.quantize(exponent, rounding=ROUND_HALF_UP)
	#try
	
	except (InvalidOperation, ValueError):
		# If the text is "ABC" or something unparseable, return None
		return None
	#except
	
#def 


