from django.test import TestCase

from VRRTController.models import Survey
from VRRTController.models import SurveyInstance
from VRRTController.models import SiteID

# Create your tests here.

# Survey Model Tests - 100% coverage
class SurveyTestClass(TestCase):
    @classmethod
    def setUpTestData(cls):
        Survey.objects.create(SurveyName='VRRTSurvey')
        pass
    def test_survey_name_label(self):
        # Get a survey object to test
        survey = Survey.objects.get(id=1)

        # Get the metadata for the required field and use it to query the required field data
        field_label = survey._meta.get_field('SurveyName').verbose_name

        # Compare the value to the expected result
        self.assertEqual(field_label, 'SurveyName')
    def test_survey_name_max_length(self):
        # Get a survey object to test
        survey = Survey.objects.get(id=1)

        # Get the metadata for the required field and use it to query the required field data
        max_length = survey._meta.get_field('SurveyName').max_length

        # Compare the value to the expected result
        self.assertEqual(max_length, 200)

# Tests for Site ID Model: 100% Coverage
class SiteIDTestClass(TestCase):
    @classmethod
    def setUpTestData(cls):
        SiteID.objects.create(SiteName='Reno', SiteAddress='123 Apple St', SiteState='NV', SiteCity='Reno', SiteZipCode='89503', SiteTelephone='775-555-5555')
        pass
    # Validating the field labels are as expected
    def test_site_name_label(self):
        siteID = SiteID.objects.get(id=1)
        field_label = siteID._meta.get_field('SiteName').verbose_name
        self.assertEqual(field_label, 'SiteName')
    def test_site_address_label(self):
        siteID = SiteID.objects.get(id=1)
        field_label = siteID._meta.get_field('SiteAddress').verbose_name
        self.assertEqual(field_label, 'SiteAddress')
    def test_site_state_label(self):
        siteID = SiteID.objects.get(id=1)
        field_label = siteID._meta.get_field('SiteState').verbose_name
        self.assertEqual(field_label, 'SiteState')
    def test_site_city_label(self):
        siteID = SiteID.objects.get(id=1)
        field_label = siteID._meta.get_field('SiteCity').verbose_name
        self.assertEqual(field_label, 'SiteCity')
    def test_site_zip_label(self):
        siteID = SiteID.objects.get(id=1)
        field_label = siteID._meta.get_field('SiteZipCode').verbose_name
        self.assertEqual(field_label, 'SiteZipCode')
    def test_site_telephone_label(self):
        siteID = SiteID.objects.get(id=1)
        field_label = siteID._meta.get_field('SiteTelephone').verbose_name
        self.assertEqual(field_label, 'SiteTelephone')
    # Validating that the size of the char fields are as expected
    def test_site_name_max_length(self):
        siteID = SiteID.objects.get(id=1)
        max_length = field_label = siteID._meta.get_field('SiteName').max_length
        self.assertEqual(max_length, 200)
    def test_site_address_max_length(self):
        siteID = SiteID.objects.get(id=1)
        max_length = field_label = siteID._meta.get_field('SiteAddress').max_length
        self.assertEqual(max_length, 200)
    def test_site_state_max_length(self):
        siteID = SiteID.objects.get(id=1)
        max_length = field_label = siteID._meta.get_field('SiteState').max_length
        self.assertEqual(max_length, 200)
    def test_site_city_max_length(self):
        siteID = SiteID.objects.get(id=1)
        max_length = field_label = siteID._meta.get_field('SiteCity').max_length
        self.assertEqual(max_length, 200)
    def test_site_zip_max_length(self):
        siteID = SiteID.objects.get(id=1)
        max_length = field_label = siteID._meta.get_field('SiteZipCode').max_length
        self.assertEqual(max_length, 200)
    def test_site_telephone_max_length(self):
        siteID = SiteID.objects.get(id=1)
        max_length = field_label = siteID._meta.get_field('SiteTelephone').max_length
        self.assertEqual(max_length, 200)
    

class SurveyInstanceTestClass(TestCase):
    @classmethod
    def setUpTestData(cls):
        SurveyInstance.objects.create(survey=Survey.objects.create(SurveyName='VRRTSurvey'),id= 'f2838392-2966-4b45-a13f-f46125c961f6', PatientID='VA_01_01', PainScoreStart=9, PainScoreEnd=8, HeartRateStart=75, HeartRateEnd=65, BPStartValue1=140, BPStartValue2=138, BPEndValue1=70, BPEndValue2=68, O2SaturationStart=98, O2SaturationEnd=99, RespirationRateStart=14, RespirationRateEnd=13, RestlessnessStart=True, RestlessnessEnd=True, DepressionStart=True, DepressionEnd=True, NauseaStart=False, NauseaEnd=True, AnxietyStart=True, AnxietyEnd=False, VisiblePainStart=True, VisiblePainEnd=False, TremorsStart=False, TremorsEnd=False, DelusionsStart=False, DelusionsEnd=False, TherapyDuration=30)
        pass
    # Label validation
    def test_survey_instance_hr_start_label(self):
        form = SurveyInstance()
        self.assertEqual(form._meta.get_field('HeartRateStart').verbose_name, 'HeartRateStart')
    def test_survey_instance_hr_end_label(self):
        form = SurveyInstance()
        self.assertEqual(form._meta.get_field('HeartRateEnd').verbose_name, 'HeartRateEnd')
    def test_survey_instance_bp_start1_label(self):
        form = SurveyInstance()
        self.assertEqual(form._meta.get_field('BPStartValue1').verbose_name, 'BPStartValue1')
    def test_survey_instance_bp_start2_label(self):
        form = SurveyInstance()
        self.assertEqual(form._meta.get_field('BPStartValue2').verbose_name, 'BPStartValue2')
    def test_survey_instance_bp_end1_label(self):
        form = SurveyInstance()
        self.assertEqual(form._meta.get_field('BPEndValue1').verbose_name, 'BPEndValue1')
    def test_survey_instance_bp_end2_label(self):
        form = SurveyInstance()
        self.assertEqual(form._meta.get_field('BPEndValue2').verbose_name, 'BPEndValue2')
    def test_survey_instance_o2_start_label(self):
        form = SurveyInstance()
        self.assertEqual(form._meta.get_field('O2SaturationStart').verbose_name, 'O2SaturationStart')
    def test_survey_instance_o2_end_label(self):
        form = SurveyInstance()
        self.assertEqual(form._meta.get_field('O2SaturationEnd').verbose_name, 'O2SaturationEnd')
    def test_survey_instance_rr_start_label(self):
        form = SurveyInstance()
        self.assertEqual(form._meta.get_field('RespirationRateStart').verbose_name, 'RespirationRateStart')
    def test_survey_instance_rr_end_label(self):
        form = SurveyInstance()
        self.assertEqual(form._meta.get_field('RespirationRateEnd').verbose_name, 'RespirationRateEnd')
    # Help Text Validation
    def test_survey_instance_hr_start_help_text(self):
        form = SurveyInstance()
        self.assertEqual(form._meta.get_field('HeartRateStart').help_text, 'Heart Rate at the start of session')
    def test_survey_instance_hr_end_help_text(self):
        form = SurveyInstance()
        self.assertEqual(form._meta.get_field('HeartRateEnd').help_text, 'Heart Rate at the end of session')
    def test_survey_instance_bp_start1_help_text(self):
        form = SurveyInstance()
        self.assertEqual(form._meta.get_field('BPStartValue1').help_text, 'Blood Pressure value1 at the start of session')
    def test_survey_instance_bp_start2_help_text(self):
        form = SurveyInstance()
        self.assertEqual(form._meta.get_field('BPStartValue2').help_text, 'Blood Pressure value2 at the start of session')
    def test_survey_instance_bp_end1_help_text(self):
        form = SurveyInstance()
        self.assertEqual(form._meta.get_field('BPEndValue1').help_text, 'Blood Pressure value1 at the end of session')
    def test_survey_instance_bp_end2_help_text(self):
        form = SurveyInstance()
        self.assertEqual(form._meta.get_field('BPEndValue2').help_text, 'Blood Pressure value2 at the end of session')
    def test_survey_instance_o2_start_help_text(self):
        form = SurveyInstance()
        self.assertEqual(form._meta.get_field('O2SaturationStart').help_text, 'Oxygen saturation level at start of session')
    def test_survey_instance_o2_end_help_text(self):
        form = SurveyInstance()
        self.assertEqual(form._meta.get_field('O2SaturationEnd').help_text, 'Oxygen saturation level at the end of session')
    def test_survey_instance_rr_start_help_text(self):
        form = SurveyInstance()
        self.assertEqual(form._meta.get_field('RespirationRateStart').help_text, 'Resperation rate at the start of session')
    def test_survey_instance_rr_end_help_text(self):
        form = SurveyInstance()
        self.assertEqual(form._meta.get_field('RespirationRateEnd').help_text, 'Resperation rate at the end of session')
