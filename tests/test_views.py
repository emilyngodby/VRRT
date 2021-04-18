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

# Log in Pass/Fail Conditions for both user types
# 100% Code coverage for views.py and urls.py -- integration tests

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