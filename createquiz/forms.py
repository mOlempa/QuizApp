from django import forms
from django.forms import inlineformset_factory
from uploader.models import Quiz, Question, Answer

class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['name']

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text']

# This creates a set of Answer forms linked to a single Question
AnswerFormSet = inlineformset_factory(
    Question, 
    Answer, 
    fields=['text', 'is_correct'], 
    extra=1,        # Number of empty answer slots to show
    can_delete=True # Allows users to remove an answer slot
)