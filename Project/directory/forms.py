from django import forms

from .models import Context, Question, Answer, TopicNames, Topics


class ContextForm(forms.ModelForm):
	
	class Meta:
		model = Context
		fields = ['context_id', 'context_title', 'context']
	#class Meta	
	
#class ContextForm



class QuestionForm(forms.ModelForm):
	
	class Meta:
		model = Question
		fields = ['q_id', 'question', 'target_level', 'question_difficulty', 'question_discrimination', 'question_facility']
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


class TopicsNamesForm(forms.ModelForm):
	
	class Meta:
		model = TopicNames
		fields = ['name']
	#class Meta
	
#class


class TopicsForm(forms.ModelForm):
	
	class Meta:
		model = Topics
		fields = []
	#class Meta
	
#class

