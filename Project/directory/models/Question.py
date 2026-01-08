from django.db import models

class Question(models.Model):
	
	question = models.CharField(null=False, default=None, max_length=516)
	
	def __str__(self):
		return f"{self.question}"
	#def __str__
	
#class Question
