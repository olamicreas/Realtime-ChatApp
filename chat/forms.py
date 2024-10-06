from django import forms
from .models import Messages, Post

class MessageForm(forms.ModelForm):
    class Meta:
        model = Messages
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Type your message here...', 'id': 'id_body'}),
        }

class PostForm(forms.ModelForm):
    class Meta:
        model = Post 
        fields = ['about']
        widgets = {
            'about': forms.Textarea(attrs={'rows': 1, 'placeholder': 'Write something about yourself...', 'id': 'post'}),
        }

class SearchForm(forms.Form):
    username = forms.CharField(required=True)