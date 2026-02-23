from django.db import models

from django.conf import settings
User = settings.AUTH_USER_MODEL

class Context(models.Model):
	
	context_id = models.IntegerField(blank=False, null=False)
	context = models.TextField(null=False, default=None)
	
	uploader = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
	
	
	def __str__(self):
		return f"{self.id}"
	#def __str__
	
	
	class Meta():
		unique_together = ('uploader', 'context_id')
	#class Meta
	
#class Context