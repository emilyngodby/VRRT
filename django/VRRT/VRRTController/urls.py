from django.urls import path
from . import views


urlpatterns = [
    path('', views.logInRedirect, name='index')
]

urlpatterns += [
    path('SurveyInstance/', views.SurveyInstanceListView.as_view(), name='SurveyInstanceList'),
]

urlpatterns += [
    path('SurveyInstance/create', views.SurveyCreate.as_view(), name='Survey_Instance_Create'),
]

urlpatterns += [
    path('missionStatment', views.MissionStatmentView.as_view(), name="Mission_Statment"),
]

urlpatterns += [
    path('SiteIDList/', views.SiteListView.as_view(), name='Site_List_View')
]

urlpatterns += [
    path('logInRedirect', views.logInRedirect, name='logInRedirect'),
]

urlpatterns += [
    path('staffLandingPage', views.staffLandingPage.as_view(), name='staffLandingPage')
]

urlpatterns += [
    path('patientLandingPage', views.patientLandingPage.as_view(), name='patientLandingPage')
]
urlpatterns += [
    path('surveyInputPage', views.surveyInputPage.as_view(), name='surveyInputPage')
]
urlpatterns += [
    path('adminProgressPage', views.adminProgressPage.as_view(), name='adminProgressPage')
]
urlpatterns += [
    path('adminProgressPreviewPage', views.adminProgressPreviewPage.as_view(), name='adminProgressPreviewPage')
]
urlpatterns += [
    path('patientProgressPage', views.patientProgressPage.as_view(), name='patientProgressPage')
]
urlpatterns += [
    path('chatbotPage', views.chatbotPage.as_view(), name='chatbotPage')
]



# urlpatterns += [
#     path('SurveyInstance/', views.SurveyInstanceListView.as_view(), name='SurveyInstanceList')
#     #path('SurveyInstance/<int:pk>', views.SurveyInstanceDetailView.as_view(), name='Survey-Instance-detail'),
# ]
