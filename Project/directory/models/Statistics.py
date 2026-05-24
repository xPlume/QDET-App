from django.db import models

from django.conf import settings
User = settings.AUTH_USER_MODEL

from directory.models import TrainedModel


class Statistic(models.Model):
	
	# Foreign Keys
	user = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
	model_used = models.ForeignKey(TrainedModel, null=False, on_delete=models.CASCADE)
	
	# Attributes
	mean = models.DecimalField(max_digits=4, decimal_places=2, null=False, blank=False)
	std_error = models.DecimalField(max_digits=4, decimal_places=2, null=False, blank=False)
	median = models.DecimalField(max_digits=4, decimal_places=2, null=False, blank=False)
	mode = models.DecimalField(max_digits=4, decimal_places=2, null=False, blank=False)
	std_deviation = models.DecimalField(max_digits=4, decimal_places=2, null=False, blank=False)
	variance = models.DecimalField(max_digits=4, decimal_places=2, null=False, blank=False)
	kurtosis = models.DecimalField(max_digits=4, decimal_places=2, null=False, blank=False)
	skewness = models.DecimalField(max_digits=4, decimal_places=2, null=False, blank=False)
	minimum = models.DecimalField(max_digits=4, decimal_places=2, null=False, blank=False)
	maximum = models.DecimalField(max_digits=4, decimal_places=2, null=False, blank=False)
	range = models.DecimalField(max_digits=4, decimal_places=2, null=False, blank=False)
	count = models.IntegerField(null=False, blank=False)
	
	created_at = models.DateTimeField(auto_now_add=True)
	
	
	def __str__(self):
		return f"Statisctics for {self.model_used.title}"
	#def 
	
#class
