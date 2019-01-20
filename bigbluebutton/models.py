from django.db import models
from hashlib import sha1
from urllib import parse, request
from bs4 import BeautifulSoup
from django.conf import settings
from django.contrib import messages




def soup_api(req):
        source = request.urlopen(req).read()
        soup = BeautifulSoup(source, 'xml')
        result = soup.find('returncode').text

        try:
            if result == 'SUCCESS':
                return source
            elif soup.find('returncode').text == 'FAILED':
                return soup.find('messagekey').text + ' : '+ soup.find('message').text
            else:
                return 'Error Api'
        except:
            return None

#=== -> create meeting url===========================================

# === <- create_paramater_for url ====================================
def create_paramater_url(call_api, parameters):

    checksum_val = sha1(str(call_api + parameters + settings.BBB_SECRET).encode('utf-8')).hexdigest()

    result = '%s&checksum=%s' % (parameters, checksum_val)
    return result

# === <- create_paramater_for url =========================================


# === -> catch error messages from in api ==================================



class BBBMeeting(models.Model):

    name = models.CharField(max_length=100, unique=True)
    meetingID = models.CharField(max_length=100, unique=True)
    attendeePW = models.CharField(max_length=100, unique=True)
    moderatorPW = models.CharField(max_length=100, unique=True)
    duration = models.IntegerField(blank=False,  default=None)
    record= models.BooleanField(blank=False, default=None)
    allowStartStopRecording = models.BooleanField(blank=False, default=None)
    welcome = models.CharField(max_length=500, blank=False, default=None)
    running=models.BooleanField(blank=False, default=False)


    def __str__(self):
        return self.name

   # === -> model field to url  ================================

    @classmethod
    def modelfield_to_url(self, meeting):
        parameters={}
        for field in meeting._meta.get_fields():
            if field.name != 'id' and field.name != 'running':
                parameters.update({
                    field.name: getattr(meeting, field.name),
                })
        return parse.urlencode(parameters)

    # === <-  model field to url  ================================


    # === -> request post to url  ================================
    @classmethod
    def request_to_url(self, request):
        request.POST._mutable = True;
        request.POST.pop('csrfmiddlewaretoken')
        return request.POST.urlencode()

    # === <- request post to url ===================================


    # === -> create meeting ==============================================
    @classmethod
    def create_meeting(self, parameters):
        call_api = 'create'
        secret_url =create_paramater_url(call_api, parameters)
        url_api = settings.BBB_URL+call_api+'?'+secret_url
        result = soup_api(url_api)
        if result:
            return result
        else:
            raise

    # === <- create meeting ==============================================


    # === -> join meeting ==============================================
    @classmethod
    def join_meeting(self, meeting_id, password, full_name):
        call_api = 'join'
        parameters=parse.urlencode({
            'meetingID': meeting_id,
            'password' : password,
            'fullName' : full_name,
        })

        secret_url = create_paramater_url(call_api, parameters)
        url_api = settings.BBB_URL+call_api+'?'+secret_url
        return url_api

    # === <- join meeting ==============================================



    # === <- end meeting ==============================================
    @classmethod
    def end_meeting(self, meeting_id, password):
        call_api='end'
        parameters = parse.urlencode({
            'meetingID': meeting_id,
            'password' : password,
        })

        secret_url = create_paramater_url(call_api, parameters)
        url_api = settings.BBB_URL+call_api+'?'+secret_url
        result = soup_api(url_api)

        if result:
            return result
        else:
            raise

    # === <- end meeting ==============================================


    # === -> meeting list ==============================================
    @classmethod
    def get_meetings_list(self):
        call_api ='getMeetings'
        parameters=''
        url_api = settings.BBB_URL+call_api+'?'+ create_paramater_url(call_api, parameters)
        result = soup_api(url_api)

        if result:
            soup = BeautifulSoup(result, 'xml')
            meetinglist = soup.find_all('meeting')
            meetings= []
            for meeting in meetinglist:
                meetings.append({
                    'meetingID' : meeting.find('meetingID').text,
                    'moderaotorPW' : meeting.find('moderatorPW').text,
                    'duration' : meeting.find('duration').text,
                    'running': meeting.find('running').text,
                    'createtime': meeting.find('createTime').text
                })
            return meetings
        else:
            return 'error: not found result of meeting list'

    # === <- meeting list  ==============================================


    # === -> get meeting info ==============================================
    @classmethod
    def get_meeting_info(self, meetingID, password):
        call_api = 'getMeetingInfo'
        parameters =parse.urlencode({
            'meetingID': meetingID,
            'password' : password,
        })

        secret_url = create_paramater_url(call_api, parameters)
        url_api = settings.BBB_URL+call_api+'?'+secret_url
        result = soup_api(url_api)
        soup = BeautifulSoup(result, 'xml')
        info={}
        if result:
                info['meetingName']=soup.find('meetingName').text,
                info['meetingID']=soup.find('meetingID').text,
                info['internalMeetingID']=soup.find('internalMeetingID').text,
                info['createDate']=soup.find('createDate').text,
                info['attendeePW']=soup.find('attendeePW').text,
                info['moderatorPW']=soup.find('moderatorPW').text,
                info['duration']=soup.find('duration').text,
                info['recording']=soup.find('recording').text,
                # info['startTime']= soup.find('startTime'),
                # info['endTime']= soup.find('endTime').text,
                info['attendees']= soup.find('attendees').text


        return info




    # === -> get meeting info ==============================================



    # === -> is running meeting ==============================================
    @classmethod
    def is_running(meetingID):
        call_api ='isMeetingRunning'
        parameters = parse.urlencode({'meetingID': meetingID})
        url_api = settings.BBB_URL + call_api + '?' + create_paramater_url(call_api, parameters)
        result = soup_api(url_api)

        if result:
            soup = BeautifulSoup(result, 'xml')
            soup = soup.find('running').text
            return soup
        else:
            return 'error'

    #=== <- catch error messages from in api ==============================================
    @classmethod
    def catch_messages(self, request, result):
        soup = BeautifulSoup(result, 'xml')
        if not soup.find('returncode'):
            return messages.warning(request, result)
        else:
            if soup.find('returncode').text == 'SUCCESS' and soup.find('messageKey').text == '':
                return messages.success(request, 'succesfully')
            else:
                return messages.warning(request, soup.find('messageKey').text + ': ' + soup.find('message').text)

    # === <- catch error messages from in api ==================================


    # print(create_meeting('wew','we','ap', 'mp'))
    # print('join meet mod->'+join_meeting('we', 'mp', 'v user'))
    #print(end_meeting('aerzt', 'mp'))
    # print('isrunning->'+is_running('tpid'))
    # print(get_meetings_list())
    # source = request.urlopen('http://192.168.1.102/bigbluebutton/').read()
    # soup = BeautifulSoup(source, 'xml')
    

