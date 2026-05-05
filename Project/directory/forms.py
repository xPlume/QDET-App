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


# Allowing the user to choose parameters to train the model
class TrainModelForm(forms.Form):
	
	# The new Select field
	PARAM_CHOICES = [
		('1', 'Question Difficulty'),
		('2', 'Question Discrimination'),
		('3', 'Question Facility'),
	]
	param_selection = forms.ChoiceField(choices=PARAM_CHOICES, required=True)
	
#class

# Requesting info from the user to save the
# trained model as a pickle file in the DB
class SaveTrainedModelForm(forms.Form):
	title = forms.CharField(max_length=255)
	public = forms.BooleanField(required=False)
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




