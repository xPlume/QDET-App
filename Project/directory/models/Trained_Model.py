from django.db import models
import os
import uuid

from django.conf import settings
User = settings.AUTH_USER_MODEL


def pickle_file_path(instance, filename):
	return os.path.join("users", f"{instance.uploader.id}", filename)
#def 


class TrainedModel(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	title = models.CharField(max_length=255)
	trained_at = models.DateTimeField(auto_now_add=True)
	public = models.BooleanField(default=False)
	
	# The 'upload_to' argument organizes files into a subfolder
	pickle_file = models.FileField(upload_to=pickle_file_path)
	
	
	uploader = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
	
	def __str__(self):
		return f"{self.title} - {self.id}"
	#def
	
	
	# When deleting model reference, delete pickle from media folder 
	def delete(self, *args, **kwargs):
		if self.pickle_file and os.path.isfile(self.pickle_file.path):
			os.remove(self.pickle_file.path)
		#if
		super().delete(*args, **kwargs)
	#def
	
#class