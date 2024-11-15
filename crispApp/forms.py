from django.forms import ModelForm, DateInput
from .models import Todo

class TodoForm(ModelForm):
     class Meta:
          model = Todo
          fields = ['title', 'memo', 'important','visibility']
          widgets = {
            'complete_by': DateInput(attrs={'type': 'date'}),
          }