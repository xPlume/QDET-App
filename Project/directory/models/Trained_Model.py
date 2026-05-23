from django.db import models
import os
import uuid

from django.db.models.signals import post_delete
from django.dispatch import receiver

from directory.utils import ParameterChoices
from django.conf import settings
User = settings.AUTH_USER_MODEL


def pickle_file_path(instance, filename):
	return os.path.join("users", f"{instance.uploader.id}", "Pickle", filename)
#def 


class TrainedModel(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	title = models.CharField(max_length=255)
	trained_at = models.DateTimeField(auto_now_add=True)
	public = models.BooleanField(default=False)
	
	parameter = models.CharField(choices=ParameterChoices.choices, default=None, max_length=63)
	
	# The 'upload_to' argument organizes files into a subfolder
	pickle_file = models.FileField(upload_to=pickle_file_path)
	
	
	uploader = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
	
	def __str__(self):
		return f"{self.title} - {self.id}"
	#def
	
#class


# Makes sure pickle file is deleted when object is deleted (even on bulk-delete)
@receiver(post_delete, sender=TrainedModel)
def delete_image(sender, instance, **kwargs):
	if instance.pickle_file:
		if os.path.isfile(instance.pickle_file.path):
			os.remove(instance.pickle_file.path)
		#if
	#if
#def