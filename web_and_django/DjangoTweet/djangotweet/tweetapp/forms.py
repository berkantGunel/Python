from django import forms
from django.forms import ModelForm
from tweetapp.models import Tweet


class AddTweetForm(forms.Form):
    nickname_input = forms.CharField(label="Username: ", max_length=50)
    message_input = forms.CharField(label="Message: ", max_length=100)
  

class AddTweetModelForm(ModelForm):
    class Meta:
        model = Tweet
        fields = ["username","message"]