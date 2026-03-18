from django.db import models
from directory.models import Question


class Answer(models.Model):
	
	question_linked = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)
	answer = models.TextField(null=False, default=None)
	is_correct = models.BooleanField(default=False)
	
	def __str__(self):
		return f"{self.answer}"
	#def __str__
	
#class Answer