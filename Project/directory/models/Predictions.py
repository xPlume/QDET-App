from django.db import models

from directory.models import Question, TrainedModel
from directory.parameters import ParameterChoices
from django.conf import settings
User = settings.AUTH_USER_MODEL

class Prediction(models.Model):
	
	question = models.ForeignKey(Question, null=False, on_delete=models.CASCADE)
	model_used = models.ForeignKey(TrainedModel, null=False, on_delete=models.CASCADE)
	
	value = models.DecimalField(max_digits=6, decimal_places=4, null=False, blank=False)
	created_at = models.DateTimeField(auto_now_add=True)
	
	parameter = models.CharField(choices=ParameterChoices.choices, default=None, max_length=63)
	
	user = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
	
	
	def __str__(self):
		return f"Model: [{self.parameter}]{self.model_used.title}; {self.question.q_id}; Predicted value: {self.value}"
	#def __str__
	
#class Question
