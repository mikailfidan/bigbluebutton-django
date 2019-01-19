from .models import BBBMeeting
from django import forms

class CreateMeetingForm(forms.ModelForm):
    # name = forms.CharField(max_length=100,  widget=forms.TextInput(attrs={'class': 'form-control'}))
    # meetingID = forms.CharField(max_length=100,  widget=forms.TextInput(attrs={'class': 'form-control'}))
    # attendeePW = forms.CharField(max_length=100,  widget=forms.TextInput(attrs={'class': 'form-control'}))
    # moderatorPW = forms.CharField(max_length=100,  widget=forms.TextInput(attrs={'class': 'form-control'}))
    # duration = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    # record= forms.BooleanField(initial=True, label='record', required=False, widget=forms.CheckboxInput(attrs={'class': 'form-control col-sm-2 mt-2'}))
    # allowStartStopRecording = forms.BooleanField(label='Allow Record', required=False, widget=forms.CheckboxInput(attrs={'class': 'form-control col-sm-2 mt-2'}))
    # welcome = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '1'}))

    class Meta:
        model = BBBMeeting
        exclude = ['running', 'create_url']



class Joinform(forms.Form):
    meeting_id = forms.CharField()
    full_name = forms.CharField()
    passwd = forms.CharField()