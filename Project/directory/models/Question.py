from django.db import models

from django.conf import settings
User = settings.AUTH_USER_MODEL

from directory.models import Context

class Question(models.Model):
	
	q_id = models.TextField(null=False, default=None)
	question = models.TextField(null=False, default=None)
	target_level = models.TextField(null=False, default=None)
	question_difficulty = models.DecimalField(max_digits=4, decimal_places=2, null=True)
	question_discrimination = models.DecimalField(max_digits=4, decimal_places=1, null=True)
	question_facility = models.DecimalField(max_digits=4, decimal_places=1, null=True)
	
	uploader = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
	context = models.ForeignKey(Context, null=False, on_delete=models.CASCADE)
	
	
	def __str__(self):
		return f"{self.id}"
	#def __str__
	
#class Question
