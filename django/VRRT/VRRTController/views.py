from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic.detail import DetailView
from VRRTController.models import Survey, SurveyInstance, SiteID
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import JsonResponse
from chatterbot import ChatBot
from chatterbot.ext.django_chatterbot import settings
import json


"""
************************ METHODS ************************
"""

"""
pageUserAuth(request,neededGroup,pageTemplate,context=None)

The page User Auth function takes 4 paramaters
-request(pass in the request from the view function this is being called from)
-neededGroup is a string that is the name of the group the user needs to be in to access the current page Ex: neeededGroup = 'Staff'
-pageTemplate is a string that is the html file for the page that will be loaded if the user is apart of the correct group
-context This is a arr and is set to none by dafult and is not needed, only used in views where we are retreving data such as survey list

"""

def pageUserAuth(request,neededGroup,pageTemplate,context=None):

    userGroup = request.user.groups.filter(user=request.user)[0]
    userGroup = str(userGroup)
    print("PageUserAuth: context: " + str(context))
    print("PageUserAuth: userGroup: " + str(userGroup))
    print("PageUserAuth: pageTemplate: " + str(pageTemplate))

    if context == None:
        print("PageUserAuth: context is empty")
        if userGroup == neededGroup:
            print("PageUserAuth: Group Check Passed")
            return render(request,pageTemplate)
        elif userGroup == 'Staff':
            print("PageUserAuth: Group Check Failed")
            return HttpResponseRedirect(reverse_lazy('staffLandingPage'))
        elif userGroup == 'Patient':
            print("PageUserAuth: Group Check Failed")
            return HttpResponseRedirect(reverse_lazy('patientLandingPage'))
        else:
            return HttpResponseRedirect(reverse_lazy('logout'))
    elif context != None:
        print("PageUserAuth: context is NOT empty")
        if userGroup == neededGroup:
            print("PageUserAuth: Group Check Passed")
            return render(request,pageTemplate)
        elif userGroup == 'Staff':
            print("PageUserAuth: Group Check Failed")
            return HttpResponseRedirect(reverse_lazy('staffLandingPage'))
        elif userGroup == 'Patient':
            print("PageUserAuth: Group Check Failed")
            return HttpResponseRedirect(reverse_lazy('patientLandingPage'))
        else:
            return HttpResponseRedirect(reverse_lazy('logout'))


""" 

************************ NON LOGIN VIEWS ************************

"""



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
    


class MissionStatmentView(generic.View):
    def get(self, request):
        return render(request, "mission_statment.html")

class SiteListView(generic.ListView):
    model = SiteID



""" 

************************ STAFF VIEWS ************************

"""

class staffLandingPage(LoginRequiredMixin, generic.View):

    login_url = 'login'
    redirect_field_name = 'login'

    def get(self, request):

        userGRoup = request.user.groups.filter(user=request.user)[0]

        return pageUserAuth(request,'Staff',"admin_landing_pg.html")


class adminProgressPage(LoginRequiredMixin, generic.View):

    login_url = 'login'
    redirect_field_name = 'login'

    def get(self, request):

        return pageUserAuth(request,'Staff',"admin_progress.html")

        return render(request, "admin_progress.html")


class adminProgressPreviewPage(LoginRequiredMixin, generic.View):

    login_url = 'login'
    redirect_field_name = 'login'

    def get(self, request):

        return pageUserAuth(request,'Staff',"admin_progress_preview.html")

        return render(request, "admin_progress_preview.html")

class surveyInputPage(LoginRequiredMixin, generic.View):

    login_url = 'login'
    redirect_field_name = 'login'

    def get(self, request):

        return pageUserAuth(request,'Staff',"survey_input.html")

        return render(request, "survey_input.html")

class surveyVerifyPage(LoginRequiredMixin, generic.View):

    login_url = 'login'
    redirect_field_name = 'login'

    def get(self, request):

        return pageUserAuth(request,'Staff',"survey_verify.html")

        return render(request, "survey_verify.html")


"""
    These two functions are from before and need to be updated
"""

class SurveyInstanceListView(generic.ListView):
    model = SurveyInstance 
    
class SurveyCreate(CreateView):
    model = SurveyInstance
    fields = ['PainScoreStart','PainScoreEnd', 'HeartRateStart', 
        'HeartRateEnd', 'BPStartValue1', 'BPStartValue2', 
        'BPEndValue1', 'BPEndValue2', 'O2SaturationStart',
        'O2SaturationEnd']
    success_url = reverse_lazy('index')



""" 

************************ PATIENT VIEWS ************************

"""

class patientLandingPage(LoginRequiredMixin, generic.View):

    login_url = 'login'
    redirect_field_name = 'login'

    def get(self, request):

        return pageUserAuth(request,'Patient',"patient_landing_page.html")

        return render(request, "patient_landing_page.html")


class patientProgressPage(LoginRequiredMixin, generic.View):

    login_url = 'login'
    redirect_field_name = 'login'

    def get(self, request):

        return pageUserAuth(request,'Patient',"patient_progress.html")

        return render(request, "patient_progress.html")

class chatbotPage(LoginRequiredMixin, generic.View):

    login_url = 'login'
    redirect_field_name = 'login'

    def get(self, request):

        return pageUserAuth(request,'Patient',"chatbot.html")

        return render(request, "chatbot.html")

class ChatterBotApiView(generic.View):
    """
    Provide an API endpoint to interact with ChatterBot.
    """

    chatterbot = ChatBot(**settings.CHATTERBOT)

    def post(self, request, *args, **kwargs):
        """
        Provide an API endpoint to interact with ChatterBot.
        """

        chatterbot = ChatBot(**settings.CHATTERBOT)

        def post(self, request, *args, **kwargs):
            """
            Return a response to the statement in the posted data.

            * The JSON data should contain a 'text' attribute.
            """
            input_data = json.loads(request.body.decode('utf-8'))

            if 'text' not in input_data:
                return JsonResponse({
                    'text': [
                        'The attribute "text" is required.'
                    ]
                }, status=400)

            response = self.chatterbot.get_response(input_data)

            response_data = response.serialize()

            return JsonResponse(response_data, status=200)

        def get(self, request, *args, **kwargs):
            """
            Return data corresponding to the current conversation.
            """
            return JsonResponse({
                'name': self.chatterbot.name
            })


