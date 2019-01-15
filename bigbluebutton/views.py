from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import CreateMeetingForm, Joinform
from .models import BBBMeeting

def index(request):
    context = {
        'meetings': BBBMeeting.get_meetings_list(),
        'moderator_pw': 'mp',
        'fullname': 'Auto'
    }

    return render(request, 'bbb/index.html', context)



def create(request):
    name = request.POST.get('name'),
    meeting_id = request.POST.get('meeting_id')
    attendee_pw = request.POST.get('attendee_pw')
    moderator_pw = request.POST.get('moderator_pw')

    result = BBBMeeting.create_meeting(name, meeting_id, attendee_pw, moderator_pw)
    context = {'result': result, 'form': Joinform()}

    return render (request, 'bbb/create.html', context)



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