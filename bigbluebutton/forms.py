from django.forms import ModelForm
from .models import BBBMeeting
from django import forms

class CreateMeetingForm(forms.Form):
    name = forms.CharField(max_length=100)
    meeting_id = forms.CharField(max_length=100)
    attendee_pw = forms.CharField(max_length=100)  
    moderator_pw = forms.CharField(max_length=100)


class Joinform(forms.Form):
    meeting_id = forms.CharField()
    full_name = forms.CharField()
    passwd = forms.CharField()