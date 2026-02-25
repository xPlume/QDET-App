from django.db import models

from django.conf import settings
User = settings.AUTH_USER_MODEL

from directory.models import Question, TopicNames

class Topics(models.Model):
	
	topic_name = models.ForeignKey(TopicNames, null=False, on_delete=models.CASCADE)
	question = models.ForeignKey(Question, null=False, on_delete=models.CASCADE)
	
	def __str__(self):
		return f"{self.topic_name} by {self.topic_name.user.username}"
	#def __str__
	
#class Topics
