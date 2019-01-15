import lxml
from django.db import models
from hashlib import sha1
from urllib import parse, request
from bs4 import BeautifulSoup
from django.conf import settings




def soup_api(req):
        source = request.urlopen(req).read()
        soup = BeautifulSoup(source, 'lxml')
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




class BBBMeeting(models.Model):

    name = models.CharField(max_length=100, unique=True)
    meeting_id = models.CharField(max_length=100, unique=True)
    attendee_pw = models.CharField(max_length=100, unique=True)  
    moderator_pw = models.CharField(max_length=100, unique=True)


    # === -> get_api_url ==============================================
    @classmethod
    def get_api_url(self, call_api, parameters):
        checksum_val = sha1(str(call_api + parameters + settings.BBB_SECRET).encode('utf-8')).hexdigest()
        result = '%s&checksum=%s' % (parameters, checksum_val)
        return result

    # === <- get_api_url ==============================================



    # === -> create meeting ==============================================
    @classmethod
    def create_meeting(self, name, meeting_id, attende_pw, moderator_pw):
        call_api = 'create'
        parameters= parse.urlencode({
            'name': name,
            'meetingID': meeting_id,
            'attendeePW': attende_pw,
            'moderatorPW': moderator_pw,
        })

        secret_url =self.get_api_url(call_api, parameters)
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

        secret_url = self.get_api_url(call_api, parameters)
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

        secret_url = self.get_api_url(call_api, parameters)
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
        url_api = settings.BBB_URL+call_api+'?'+self.get_api_url(call_api, parameters)
        result = soup_api(url_api)

        if result:
            soup = BeautifulSoup(result, 'xml')
            meetinglist = soup.find_all('meeting')
            meetings= []
            for meeting in meetinglist:
                meetings.append({
                    'meeting_id' : meeting.find('meetingID').text,
                    'moderaotor_pw' : meeting.find('moderatorPW').text,
                    'attendee_pw' : meeting.find('attendeePW').text,
                    'running': meeting.find('running').text,
                    'createtime': meeting.find('createTime').text
                })
            return meetings
        else:
            return 'error: not found result of meeting list'

    # === <- meeting list  ==============================================




    # === -> is running meeting ==============================================
    def is_running(meetingID):
        call_api ='isMeetingRunning'
        parameters = parse.urlencode({'meetingID': meetingID})
        url_api = settings.BBB_URL + call_api + '?' + get_api_url(call_api, parameters)
        result = soup_api(url_api)

        if result:
            soup = BeautifulSoup(result, 'xml')
            soup = soup.find('running').text
            return soup
        else:
            return 'error'

    #=== <- get_api_url ==============================================



    # print(create_meeting('wew','we','ap', 'mp'))
    # print('join meet mod->'+join_meeting('we', 'mp', 'v user'))
    #print(end_meeting('aerzt', 'mp'))
    # print('isrunning->'+is_running('tpid'))
    # print(get_meetings_list())
    # source = request.urlopen('http://192.168.1.102/bigbluebutton/').read()
    # soup = BeautifulSoup(source, 'xml')
    

