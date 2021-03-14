from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic.detail import DetailView
from VRRTController.models import Survey, SurveyInstance, SiteID
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy




# Create your views here.



def index(request):
    """View function for home page of site"""

    #Generate count fo rthe number of active sites
    num_Sites = SiteID.objects.all().count()

    #Generate counts for number of survey types
    num_Surveys = Survey.objects.all().count()

    #Generate counts of number of surveys taken
    num_Surveys_Submitted = SurveyInstance.objects.all().count()

    context = {
        'num_Sites': num_Sites,
        'num_Surveys': num_Surveys,
        'num_Surveys_Submitted':num_Surveys_Submitted,
    }

    return render(request,'index.html',context=context)


class MissionStatmentView(generic.View):
    def get(self, request):
        return render(request, "mission_statment.html")

class SurveyInstanceListView(generic.ListView):
    model = SurveyInstance 
    
class SurveyCreate(CreateView):
    model = SurveyInstance
    fields = ['PainScoreStart','PainScoreEnd', 'HeartRateStart', 
        'HeartRateEnd', 'BPStartValue1', 'BPStartValue2', 
        'BPEndValue1', 'BPEndValue2', 'O2SaturationStart',
        'O2SaturationEnd']
    success_url = reverse_lazy('index')

class SiteListView(generic.ListView):
    model = SiteID

@login_required
def logInRedirect(request):
    group = request.user.groups.filter(user=request.user)[0]
    print(group.name)
    if group.name=="Staff":
        return HttpResponseRedirect(reverse_lazy('staffLandingPage'))
    elif group.name=="Patient":
        return HttpResponseRedirect(reverse_lazy('patientLandingPage'))

    context = {}
    template = "base_generic.html"
    return HttpResponseRedirect(reverse_lazy('index'))


class staffLandingPage(generic.View):
    def get(self, request):
        return render(request, "admin_landing_pg.html")

class patientLandingPage(generic.View):
    def get(self, request):
        return render(request, "patient_landing_page.html")

class adminProgressPage(generic.View):
    def get(self, request):
        return render(request, "admin_progress.html")

class adminProgressPreviewPage(generic.View):
    def get(self, request):
        return render(request, "admin_progress_preview.html")

class surveyInputPage(generic.View):
    def get(self, request):
        return render(request, "survey_input.html")

class surveyVerifyPage(generic.View):
    def get(self, request):
        return render(request, "survey_verify.html")

class patientProgressPage(generic.View):
    def get(self, request):
        return render(request, "patient_progress.html")

class chatbotPage(generic.View):
    def get(self, request):
        return render(request, "chatbot.html")
    


# class analyticsPage(DetailView):
#     def get(self, request)