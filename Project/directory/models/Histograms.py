import os
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver

from django.conf import settings
User = settings.AUTH_USER_MODEL

from directory.models import TrainedModel


def histograms_file_path(instance, filename):
	return os.path.join("users", f"{instance.user.id}", "Histograms", filename)
#def 


class Histogram(models.Model):
	
	chart_image = models.ImageField(upload_to=histograms_file_path)
	created_at = models.DateTimeField(auto_now_add=True)
	
	user = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
	model_used = models.ForeignKey(TrainedModel, null=False, on_delete=models.CASCADE, related_name='histograms')
	
	def __str__(self):
		return f"Histogram of {self.user.username}"
	#def 
	
#class



# Makes sure image is deleted when object is deleted (even on bulk-delete)
@receiver(post_delete, sender=Histogram)
def delete_image(sender, instance, **kwargs):
	if instance.chart_image:
		if os.path.isfile(instance.chart_image.path):
			os.remove(instance.chart_image.path)
		#if
	#if
#def