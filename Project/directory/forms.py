from django import forms

from .models import Question, Answer



class QuestionForm(forms.ModelForm):
	
	class Meta:
		model = Question
		fields = ['question']
	#class Meta	
	
#class QuestionForm


class AnswerForm(forms.ModelForm):
	
	class Meta:
		model = Answer
		fields = ['answer', 'is_correct']
	#class Meta
	
#class AnswerForm



class CSVuploadForm(forms.Form):
	
	file = forms.FileField(label='Select a .csv file')
	
#class
