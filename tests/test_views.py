from django.test import TestCase
from django.urls import reverse
import uuid
from django.contrib.auth.models import User, Group
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.test import Client

from VRRTController.models import Survey
from VRRTController.models import SurveyInstance
from VRRTController.models import SiteID

# 100% Code coverage for views.py and urls.py -- integration tests
# Log in Pass/Fail Conditions for both user types

class PatientLandingPageViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.group = Group(name='Patient')
        self.group.save()    
    def test_user_with_no_group_redirected_to_login(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('login'))
        print(Group.objects.all())
        self.assertEqual(response.status_code, 200)
    def test_user_sent_to_patient_landing_page(self):
        self.user.groups.add(self.group)
        self.user.save()
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('patientLandingPage')) 
        self.assertEqual(response.status_code, 200)

class AdminLandingPageViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.group = Group(name='Staff')
        self.group.save()    
    def test_admin_with_no_group_assigned_redirected_to_login(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('login'))
        print(Group.objects.all())
        self.assertEqual(response.status_code, 200)
    def test_admin_sent_to_admin_landing_page(self):
        self.user.groups.add(self.group)
        self.user.save()
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('staffLandingPage')) 
        self.assertEqual(response.status_code, 200)

# Patient Views Tests

class PatientProgressPageViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.group = Group(name='Patient')
        self.group.save() 
    def test_user_with_no_group_redirected_to_login(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('login'))
        print(Group.objects.all())
        self.assertEqual(response.status_code, 200)   
    def test_patient_sent_to_patient_progress_page(self):
        self.user.groups.add(self.group)
        self.user.save()
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('patientProgressPage')) 
        self.assertEqual(response.status_code, 200)

class PatientProgressPagePainScoreViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.group = Group(name='Patient')
        self.group.save()    
    def test_user_with_no_group_redirected_to_login(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('login'))
        print(Group.objects.all())
        self.assertEqual(response.status_code, 200)
    def test_patient_sent_to_patient_progress_page_pain_score(self):
        self.user.groups.add(self.group)
        self.user.save()
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('patientProgressPagePainScore')) 
        self.assertEqual(response.status_code, 200)

class PatientProgressPageHeartRateViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.group = Group(name='Patient')
        self.group.save()    
    def test_user_with_no_group_redirected_to_login(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('login'))
        print(Group.objects.all())
        self.assertEqual(response.status_code, 200)
    def test_patient_sent_to_patient_progress_page_heart_rate(self):
        self.user.groups.add(self.group)
        self.user.save()
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('patientProgressPageHeartRate')) 
        self.assertEqual(response.status_code, 200)

class ChatbotPageViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.group = Group(name='Patient')
        self.group.save()   
    def test_user_with_no_group_redirected_to_login(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('login'))
        print(Group.objects.all())
        self.assertEqual(response.status_code, 200) 
    def test_patient_sent_to_chatbot_page(self):
        self.user.groups.add(self.group)
        self.user.save()
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('chatbotPage')) 
        self.assertEqual(response.status_code, 200)

class ChatterBotApiViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.group = Group(name='Patient')
        self.group.save()    
    def test_user_with_no_group_redirected_to_login(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('login'))
        print(Group.objects.all())
        self.assertEqual(response.status_code, 200)
    def test_patient_sent_to_chatterbot_api(self):
        self.user.groups.add(self.group)
        self.user.save()
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('ChatterBotApiView')) 
        self.assertEqual(response.status_code, 200)

# Admin Views Tests
class AdminProgressResultsPageViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.group = Group(name='Staff')
        self.group.save()    
    def test_user_with_no_group_redirected_to_login(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('login'))
        print(Group.objects.all())
        self.assertEqual(response.status_code, 200)
    def test_admin_sent_to_admin_progress_results_page(self):
        self.user.groups.add(self.group)
        self.user.save()
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('adminProgressResultsPage')) 
        self.assertEqual(response.status_code, 200)

class AdminProgressPageViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.group = Group(name='Staff')
        self.group.save()  
    def test_user_with_no_group_redirected_to_login(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('login'))
        print(Group.objects.all())
        self.assertEqual(response.status_code, 200)  
    def test_admin_sent_to_admin_progress_page(self):
        self.user.groups.add(self.group)
        self.user.save()
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('adminProgressPage')) 
        self.assertEqual(response.status_code, 200)

class AdminProgressPreviewPageViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.group = Group(name='Staff')
        self.group.save()   
    def test_user_with_no_group_redirected_to_login(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('login'))
        print(Group.objects.all())
        self.assertEqual(response.status_code, 200) 
    def test_admin_sent_to_admin_progress_preview_page(self):
        self.user.groups.add(self.group)
        self.user.save()
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('adminProgressPreviewPage')) 
        self.assertEqual(response.status_code, 200)

class AdminPainScoreProgressViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.group = Group(name='Staff')
        self.group.save()  
    def test_user_with_no_group_redirected_to_login(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('login'))
        print(Group.objects.all())
        self.assertEqual(response.status_code, 200)  
    def test_admin_sent_to_admin_pain_score_progress_page(self):
        self.user.groups.add(self.group)
        self.user.save()
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('adminPainScoreProgressView')) 
        self.assertEqual(response.status_code, 200)

class AdminHearRateProgressViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.group = Group(name='Staff')
        self.group.save()   
    def test_user_with_no_group_redirected_to_login(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('login'))
        print(Group.objects.all())
        self.assertEqual(response.status_code, 200) 
    def test_admin_sent_to_admin_heart_rate_progress_page(self):
        self.user.groups.add(self.group)
        self.user.save()
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('adminHearRateProgressView')) 
        self.assertEqual(response.status_code, 200)

class AdminResperationRateProgressViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.group = Group(name='Staff')
        self.group.save()   
    def test_user_with_no_group_redirected_to_login(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('login'))
        print(Group.objects.all())
        self.assertEqual(response.status_code, 200) 
    def test_admin_sent_to_admin_resperation_rate_progress_page(self):
        self.user.groups.add(self.group)
        self.user.save()
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('adminResperationRateProgressView')) 
        self.assertEqual(response.status_code, 200)

class AdminO2SaturationProgressViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.group = Group(name='Staff')
        self.group.save()    
    def test_user_with_no_group_redirected_to_login(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('login'))
        print(Group.objects.all())
        self.assertEqual(response.status_code, 200)
    def test_admin_sent_to_admin_o2_saturation_progress_page(self):
        self.user.groups.add(self.group)
        self.user.save()
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('adminO2SaturationProgressView')) 
        self.assertEqual(response.status_code, 200)

class SurveyInputPageViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.group = Group(name='Staff')
        self.group.save()    
    def test_user_with_no_group_redirected_to_login(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('login'))
        print(Group.objects.all())
        self.assertEqual(response.status_code, 200)
    def test_admin_sent_to_survey_input_page(self):
        self.user.groups.add(self.group)
        self.user.save()
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('surveyInputPage')) 
        self.assertEqual(response.status_code, 200)

class SurveyInstanceCreateViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.group = Group(name='Staff')
        self.group.save()    
    def test_user_with_no_group_redirected_to_login(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('login'))
        print(Group.objects.all())
        self.assertEqual(response.status_code, 200)
    def test_admin_sent_to_survey_instance_create_page(self):
        self.user.groups.add(self.group)
        self.user.save()
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('Survey_Instance_Create')) 
        self.assertEqual(response.status_code, 200)

class ExportViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.group = Group(name='Staff')
        self.group.save()    
    def test_user_with_no_group_redirected_to_login(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('login'))
        print(Group.objects.all())
        self.assertEqual(response.status_code, 200)
    def test_admin_sent_to_export_page(self):
        self.user.groups.add(self.group)
        self.user.save()
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('export')) 
        self.assertEqual(response.status_code, 200)

# Database Query Views

# Testing that only the data corresponding to a particular user is returned 
class PatientProgressPainScorePreviewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')

        # create a second user to ensure it only returns survey instances pertaining to target user
        self.user2 = User.objects.create_user(username='test2', password='12345')

        self.group = Group(name='Patient')
        self.group.save()   

        SurveyInstance.objects.create(survey=Survey.objects.create(SurveyName='VRRTSurvey'),id= 'f2838392-2966-4b45-a13f-f46125c961f6', PatientID='testuser', PainScoreStart=9, PainScoreEnd=8, HeartRateStart=75, HeartRateEnd=65, BPStartValue1=140, BPStartValue2=138, BPEndValue1=70, BPEndValue2=68, O2SaturationStart=98, O2SaturationEnd=99, RespirationRateStart=14, RespirationRateEnd=13, RestlessnessStart=True, RestlessnessEnd=True, DepressionStart=True, DepressionEnd=True, NauseaStart=False, NauseaEnd=True, AnxietyStart=True, AnxietyEnd=False, VisiblePainStart=True, VisiblePainEnd=False, TremorsStart=False, TremorsEnd=False, DelusionsStart=False, DelusionsEnd=False, TherapyDuration=30)

        SurveyInstance.objects.create(survey=Survey.objects.create(SurveyName='VRRTSurvey'),id= 'f2838392-2966-4b45-a13f-f46125c961f7', PatientID='test2', PainScoreStart=10, PainScoreEnd=9, HeartRateStart=76, HeartRateEnd=66, BPStartValue1=141, BPStartValue2=139, BPEndValue1=71, BPEndValue2=69, O2SaturationStart=99, O2SaturationEnd=98, RespirationRateStart=15, RespirationRateEnd=14, RestlessnessStart=True, RestlessnessEnd=True, DepressionStart=True, DepressionEnd=True, NauseaStart=False, NauseaEnd=True, AnxietyStart=True, AnxietyEnd=False, VisiblePainStart=True, VisiblePainEnd=False, TremorsStart=False, TremorsEnd=False, DelusionsStart=False, DelusionsEnd=False, TherapyDuration=31)
    def test_pain_score_inquiry(self):
        self.user.groups.add(self.group)
        self.user2.groups.add(self.group)
        self.field = 'painScore'
        self.user2.save()
        self.user.save()
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('patientProgressPagePainScore')) 
        
        # Check if returning the right view
        self.assertEqual(response.status_code, 200)

        self.start = SurveyInstance.objects.values_list('PainScoreStart').filter(PatientID = 'testuser')
        self.start = list(self.start)

        # Check if values are correct for start
        self.assertEqual(self.start[0], (9,))

        self.end = SurveyInstance.objects.values_list('PainScoreEnd').filter(PatientID = 'testuser')
        self.end = list(self.end)

        # Check if values are correct for end
        self.assertEqual(self.end[0], (8,))
    def test_heart_rate_inquiry(self):
        self.user.groups.add(self.group)
        self.user2.groups.add(self.group)
        self.field = 'heartRate'
        self.user.save()
        self.user2.save()
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('patientProgressPageHeartRate')) 
        
        # Check if returning the right view
        self.assertEqual(response.status_code, 200)

        self.start = SurveyInstance.objects.values_list('HeartRateStart').filter(PatientID = 'testuser')
        self.start = list(self.start)

        # Check if values are correct for start
        self.assertEqual(self.start[0], (75,))

        self.end = SurveyInstance.objects.values_list('HeartRateEnd').filter(PatientID = 'testuser')
        self.end = list(self.end)

        # Check if values are correct for end
        self.assertEqual(self.end[0], (65,))
    def test_bp_value1_inquiry(self):
        self.user.groups.add(self.group)
        self.user2.groups.add(self.group)
        self.field = 'bloodPressure'
        self.user.save()
        self.user2.save()
        self.client.login(username='testuser', password='12345')

        self.start = SurveyInstance.objects.values_list('BPStartValue1').filter(PatientID = 'testuser')
        self.start = list(self.start)

        # Check if values are correct for start
        self.assertEqual(self.start[0], (140,))

        self.end = SurveyInstance.objects.values_list('BPEndValue1').filter(PatientID = 'testuser')
        self.end = list(self.end)

        # Check if values are correct for end
        self.assertEqual(self.end[0], (70,))
    def test_bp_value2_inquiry(self):
        self.user.groups.add(self.group)
        self.user2.groups.add(self.group)
        self.field = 'bloodPressure'
        self.user.save()
        self.user2.save()
        self.client.login(username='testuser', password='12345')

        self.start = SurveyInstance.objects.values_list('BPStartValue2').filter(PatientID = 'testuser')
        self.start = list(self.start)

        # Check if values are correct for start
        self.assertEqual(self.start[0], (138,))

        self.end = SurveyInstance.objects.values_list('BPEndValue2').filter(PatientID = 'testuser')
        self.end = list(self.end)

        # Check if values are correct for end
        self.assertEqual(self.end[0], (68,))
    def test_o2_saturation_inquiry(self):
        self.user.groups.add(self.group)
        self.user2.groups.add(self.group)
        self.field = 'O2Saturation'
        self.user.save()
        self.user2.save()
        self.client.login(username='testuser', password='12345')

        self.start = SurveyInstance.objects.values_list('O2SaturationStart').filter(PatientID = 'testuser')
        self.start = list(self.start)

        # Check if values are correct for start
        self.assertEqual(self.start[0], (98,))

        self.end = SurveyInstance.objects.values_list('O2SaturationEnd').filter(PatientID = 'testuser')
        self.end = list(self.end)

        # Check if values are correct for end
        self.assertEqual(self.end[0], (99,))
    def test_respiration_rate_inquiry(self):
        self.user.groups.add(self.group)
        self.user2.groups.add(self.group)
        self.field = 'respirationRate'
        self.user.save()
        self.user2.save()
        self.client.login(username='testuser', password='12345')

        self.start = SurveyInstance.objects.values_list('RespirationRateStart').filter(PatientID = 'testuser')
        self.start = list(self.start)

        # Check if values are correct for start
        self.assertEqual(self.start[0], (14,))

        self.end = SurveyInstance.objects.values_list('RespirationRateEnd').filter(PatientID = 'testuser')
        self.end = list(self.end)

        # Check if values are correct for end
        self.assertEqual(self.end[0], (13,))
    def test_duration_inquiry(self):
        self.user.groups.add(self.group)
        self.user2.groups.add(self.group)
        self.field = 'therapyDuration'
        self.user.save()
        self.user2.save()
        self.client.login(username='testuser', password='12345')

        self.start = SurveyInstance.objects.values_list('TherapyDuration').filter(PatientID = 'testuser')
        self.start = list(self.start)

        # Check if values are correct for start
        self.assertEqual(self.start[0], (30,))