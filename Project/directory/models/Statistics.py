from django.db import models

from django.conf import settings
User = settings.AUTH_USER_MODEL

from directory.models import TrainedModel


class Statistic(models.Model):
	
	# Foreign Keys
	user = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
	model_used = models.ForeignKey(TrainedModel, null=False, on_delete=models.CASCADE, related_name='statistics')
	
	# Attributes
	mean = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
	std_error = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
	median = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
	mode = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
	std_deviation = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
	variance = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
	kurtosis = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
	skewness = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
	minimum = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
	maximum = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
	range = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
	count = models.IntegerField(null=True, blank=True)
	
	created_at = models.DateTimeField(auto_now_add=True)
	
	
	def __str__(self):
		return f"Statisctics for {self.model_used.title}"
	#def 
	
#class
