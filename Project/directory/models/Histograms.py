import os
from django.db import models

from django.conf import settings
User = settings.AUTH_USER_MODEL

from directory.models import TrainedModel


def histograms_file_path(instance, filename):
	return os.path.join("users", f"{instance.user.id}", filename)
#def 


class Histogram(models.Model):
	
	chart_image = models.ImageField(upload_to=histograms_file_path)
	created_at = models.DateTimeField(auto_now_add=True)
	
	user = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
	model_used = models.ForeignKey(TrainedModel, null=False, on_delete=models.CASCADE)
	
	def __str__(self):
		return f"Histogram of {self.user.username}"
	#def 
	
#class