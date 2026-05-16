from django.db import models



class ParameterChoices(models.TextChoices):
	
	# NAME = 'database_value', 'human-readable_label'
	DIFFICULTY = 'difficulty', 'Difficulty'
	DISCRIMINATION = 'discrimination', 'Discrimination'
	FACILITY = 'facility', 'Facility'
	
#class