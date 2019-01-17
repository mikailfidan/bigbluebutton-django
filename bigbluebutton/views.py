from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from urllib import parse, request
from bs4 import BeautifulSoup
from .forms import CreateMeetingForm, Joinform
from .models import BBBMeeting


def index(request):
    context = {
        'meetings': BBBMeeting.get_meetings_list(),
        'moderator_pw': 'mp',
        'fullname': 'Moderator',
        'form': CreateMeetingForm()
    }

    return render(request, 'bbb/index.html', context)


def create(request):

    if request.method == 'POST':
        form = CreateMeetingForm(request.POST)

        if form.is_valid():
            parameters = BBBMeeting.request_to_url(request)
            result = BBBMeeting.create_meeting(parameters)
            BBBMeeting.catch_messages(request, result)
        else:
            messages.warning(request, 'error occurred')
    else:
        form = CreateMeetingForm()


    context = {
        'meetings': BBBMeeting.get_meetings_list(),
        'moderator_pw': 'mp',
        'fullname': 'Moderator',
        'form': form
    }

    return render(request, 'bbb/index.html', context)



def join_meeting(request):
    meeting_id = request.POST.get('meeting_id')
    full_name = request.POST.get('full_name')
    passwd = request.POST.get('passwd')

    result = BBBMeeting.join_meeting(meeting_id, passwd, full_name)
    context = {'join_url': result}

    return render(request, 'bbb/join.html', context)



def get_join_meeting(request, meeting_id, moderator_pw, full_name) :
    url = BBBMeeting.join_meeting(meeting_id, moderator_pw, full_name)
    return redirect(url)

def end_meeting(request, meeting_id, moderator_pw):

    BBBMeeting.end_meeting(meeting_id, moderator_pw)
    print(BBBMeeting.end_meeting(meeting_id, moderator_pw))
    return redirect('/')
