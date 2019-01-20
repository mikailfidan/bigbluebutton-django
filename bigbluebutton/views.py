
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
import json

from .forms import CreateMeetingForm
from .models import BBBMeeting


def index(request):

   if request.method == 'POST':
        form = CreateMeetingForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'created succesfully')
        else:
            messages.warning(request, 'Cannot insert new meeting in database')

   open_meetings = []
   for m in BBBMeeting.get_meetings_list():
        open_meetings.append(m['meetingID'])

   context = {
        'open_meetings': open_meetings,
        'live_meetings': BBBMeeting.get_meetings_list(),
        'meetingsdb': BBBMeeting.objects.all().order_by('meetingID'),
        'form': CreateMeetingForm()
    }

   return render(request, 'bbb/index.html', context)


def create_meeting(request, meetingID):
    meeting = BBBMeeting.objects.get(meetingID=meetingID)
    parameters = BBBMeeting.modelfield_to_url(meeting)
    result = BBBMeeting.create_meeting(parameters)
    BBBMeeting.catch_messages(request, result)

    open_meetings = []
    for m in BBBMeeting.get_meetings_list():
        open_meetings.append(m['meetingID'])

    context = {
        'open_meetings': open_meetings,
        'live_meetings': BBBMeeting.get_meetings_list(),
        'meetingsdb': BBBMeeting.objects.all().order_by('meetingID'),
        'form': CreateMeetingForm()
    }

    return render(request, 'bbb/index.html', context)



def join_meeting(request, meetingID):
    meeting = BBBMeeting.objects.get(meetingID=meetingID)
    full_name = 'User-01'
    password = getattr(meeting, 'moderatorPW')

    join_url = BBBMeeting.join_meeting(meetingID, password, full_name)


    return redirect(join_url)


def end_meeting(request, meetingID):

    meeting = BBBMeeting.objects.get(meetingID=meetingID)
    password = getattr(meeting, 'moderatorPW')
    BBBMeeting.end_meeting(meetingID, password)
    return redirect('/')


def info_meeting(request, meetingID):

    meeting = BBBMeeting.objects.get(meetingID=meetingID)
    password = getattr(meeting, 'moderatorPW')
    info = BBBMeeting.get_meeting_info(meetingID, password)


    return JsonResponse(info)


