from django.contrib import admin

# Register your models here.

from .models import Survey, SurveyInstance, SiteID

admin.site.register(Survey)
admin.site.register(SurveyInstance)
admin.site.register(SiteID)