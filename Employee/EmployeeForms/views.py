from django.shortcuts import render, redirect, render_to_response
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from django.views.generic import View
from django.views.generic import CreateView
from formtools.wizard.views import SessionWizardView
from django.views.decorators.csrf import csrf_protect
from django.conf import settings
from django.contrib.auth.models import User

import json
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from models import Address, UserDetails, Education, PreviousEmployment, Proof
from forms import UserDetailsForm, EducationForm, PreviousEmploymentForm, ProofForm, UserRegistrationForm

# Create your views here.
def EmployeeWelcome(request):
    return render(request, 'welcome.html',{})

def login(request):
	context = {}
	context.update(csrf(request))
	return render_to_response('login.html',context)

def auth_view(request):
	username = request.POST.get('username','')
	password = request.POST.get('password','')
	user = auth.authenticate(username=username, password=password)

	if user is not None:
		auth.login(request, user)
		return HttpResponseRedirect('/myansrsource/loggedin')
	else:
		return HttpResponseRedirect('/myansrsource/invalid')

# def password_change(request):
#     if request.method == 'POST':
# 		form = PasswordChangeForm(request.POST)
# 		if form.is_valid():
# 			form.save()
# 			return HttpResponseRedirect('/myansrsource/password_change')
#
#     context = {}
#     context.update(csrf(request))
#
#     context['form'] = PasswordChangeForm()
#     return render_to_response(request, 'password_change.html', context)

def logout(request):
	auth.logout(request)
	return render_to_response('logout.html')

def loggedin(request):
	return render_to_response('loggedin.html',{'user':request.user.username})

def invalid_login(request):
	return render_to_response('invalid.html')

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/myansrsource/register_success')

    context = {}
    context.update(csrf(request))

    context['form'] = UserRegistrationForm()
    return render_to_response('register.html', context)

def register_success(request):
	return render_to_response('register_success.html')

# # class UserDetailsWizard(SessionWizardView):
#     template_name = "wizard.html"
#
#
#     def get_form(self, step=None, data=None, files=None):
#         form = super(UserDetailsWizard, self).get_form(step,data,files)
#         step = step if step else self.steps.current
#         if step == 'User Profile':
#
#
#         return
#
#     def get_form_initial(self,step):
#
#
#
#     def done(self, form_list, **kwargs):
#         if request.method == 'POST':
#             form = UserDetailsForm(request.POST)
#
#             if form.is_valid():
#                 employee = User.objects.get(username=request.user)
#                 first_name = form.cleaned_data['first_name']
#                 last_name = form.cleaned_data['last_name']
#                 middle_name = form.cleaned_data['middle_name']
#                 nationality = form.cleaned_data['nationality']
#                 marital_status = form.cleaned_data['marital_status']
#                 wedding_date = form.cleaned_data['wedding_date']
#                 blood_group = form.cleaned_data['blood_group']
#                 land_phone = form.cleaned_data['land_phone']
#                 emergency_phone = form.cleaned_data['emergency_phone']
#                 mobile_phone = form.cleaned_data['mobile_phone']
#                 personal_email = form.cleaned_data['personal_email']
#                 gender = form.cleaned_data['gender']
#
#                 UserDetails(employee = employee,
#                 middle_name=middle_name,
#                 nationality=nationality,
#                 marital_status=marital_status,
#                 wedding_date=wedding_date,
#                 blood_group=blood_group,
#                 land_phone=land_phone,
#                 emergency_phone=emergency_phone,
#                 mobile_phone=mobile_phone,
#                 personal_email=personal_email).save()
#
#         context.update(csrf(request))
#
#         context['form'] = form
#
#         return render(request, 'wizard.html',context)

def update(request):

    if request.method == 'GET':
        context = {'add':True, 'record_added':False, 'form':None}
        form = UserDetailsForm()
        # if request.user.is_authenticated():
        #     username = request.user.username
        user = request.user

        employee = UserDetails.objects.get(employee=user.id)
        first_name = user.first_name
        last_name = user.last_name
        middle_name = employee.middle_name
        nationality = employee.nationality
        marital_status = employee.marital_status
        wedding_date = employee.wedding_date
        blood_group = employee.blood_group
        land_phone = employee.land_phone
        emergency_phone = employee.emergency_phone
        mobile_phone = employee.mobile_phone
        personal_email = employee.personal_email
        gender = employee.gender

        context = {
        'employee':employee,
        'first_name':first_name,
        'last_name':last_name,
        'middle_name':middle_name,
        'nationality':nationality,
        'marital_status':marital_status,
        'wedding_date':wedding_date,
        'blood_group':blood_group,
        'land_phone':land_phone,
        'emergency_phone':emergency_phone,
        'mobile_phone':mobile_phone,
        'personal_email':personal_email,
        'gender':gender,
        }

        context.update(csrf(request))
#ontext = {'form':form}

        return render(request, 'wizard.html',context)

from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
@login_required
def user_details(request):

    # user details form

    if request.method == 'GET':
        #import ipdb; ipdb.set_trace()
        context = {"form":""}
        form = UserDetailsForm(request.GET)

    if request.method == 'POST':
        import ipdb; ipdb.set_trace()

        context = {"form":""}
        form = UserDetailsForm(request.POST)

        if form.is_valid():
            employee = User.objects.get(username=request.user)
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            middle_name = form.cleaned_data['middle_name']
            nationality = form.cleaned_data['nationality']
            marital_status = form.cleaned_data['marital_status']
            wedding_date = form.cleaned_data['wedding_date']
            blood_group = form.cleaned_data['blood_group']
            land_phone = form.cleaned_data['land_phone']
            emergency_phone = form.cleaned_data['emergency_phone']
            mobile_phone = form.cleaned_data['mobile_phone']
            personal_email = form.cleaned_data['personal_email']
            gender = form.cleaned_data['gender']

            UserDetails(employee = employee,
            middle_name=middle_name,
            nationality=nationality,
            marital_status=marital_status,
            wedding_date=wedding_date,
            blood_group=blood_group,
            land_phone=land_phone,
            emergency_phone=emergency_phone,
            mobile_phone=mobile_phone,
            personal_email=personal_email).save()


    context['form'] = form

    return render(request, 'wizard.html',context)

@csrf_exempt
@login_required
def education(request):
    #education form
    #import ipdb; ipdb.set_trace()
    if request.method == 'GET':
        context_data = {"education_form":""}
        education_form = EducationForm(request.GET, prefix = 'education_form')
        print request.GET



    if request.method == 'POST':
        # import ipdb; ipdb.set_trace()
        print request.POST
        context_data = {"education_form":""}
        education_form = EducationForm(request.POST, prefix = 'education_form')
        if education_form.is_valid():
            employee = User.objects.get(username=request.user)
            print employee
            qualification = education_form.cleaned_data['qualification']
            specialization = education_form.cleaned_data['specialization']
            from_date = education_form.cleaned_data['from_date']
            to_date = education_form.cleaned_data['to_date']
            institute = education_form.cleaned_data['institute']
            overall_marks = education_form.cleaned_data['overall_marks']

            Education(employee=employee,
            qualification=qualification,
            specialization=specialization,
            from_date=from_date,
            to_date=to_date,
            institute=institute,
            overall_marks=overall_marks).save()

    context_data['education_form'] = education_form

    return render(request, 'wizard.html',context_data)

    r#eturn redirect('education')

@csrf_exempt
@login_required
def proof(request):
    #proof form
    # context = {"proof_form": ""}
    if request.method == 'GET':
        context = {"proof_form":""}
        proof_form = ProofForm(request.GET, prefix="proof_form")

    if request.method == 'POST':
        import ipdb; ipdb.set_trace()
        context = {"proof_form":""}
        proof_form = ProofForm(request.POST, prefix="proof_form")
        if proof_form.is_valid():
            employee = User.objects.get(username=request.user)
            pan = proof_form.cleaned_data['pan']
            aadhar_card = proof_form.cleaned_data['aadhar_card']
            dl = proof_form.cleaned_data['dl']
            passport = proof_form.cleaned_data['passport']
            voter_id = proof_form.cleaned_data['voter_id']

            Proof(employee=employee,
            pan=pan,
            aadhar_card=aadhar_card,
            dl=dl,
            passport=passport,
            voter_id=voter_id).save()

    context['proof_form'] = proof_form

    return render(request,'wizard.html',context)

@csrf_exempt
@login_required
def previous_employment(request):
    #previous_employment form

    if request.method == 'GET':
        context = {"previous_employment_form": ""}
        previous_employment_form = PreviousEmploymentForm(request.GET, prefix="previous_employment_form")
    #import ipdb; ipdb.set_trace()

    if request.method == 'POST':
        # import ipdb; ipdb.set_trace()
        context = {"previous_employment_form":""}
        previous_employment_form = PreviousEmploymentForm(request.POST, prefix="previous_employment_form")
        if previous_employment_form.is_valid():
            employee = User.objects.get(username=request.user)
            company_name = previous_employment_form.cleaned_data['company_name']
            employed_from = previous_employment_form.cleaned_data['employed_from']
            employed_upto = previous_employment_form.cleaned_data['employed_upto']
            last_ctc = previous_employment_form.cleaned_data['last_ctc']
            reason_for_exit = previous_employment_form.cleaned_data['reason_for_exit']

            PreviousEmployment(employee=employee,
            company_name=company_name,
            employed_from=employed_from,
            employed_upto=employed_upto,
            last_ctc=last_ctc,
            reason_for_exit=reason_for_exit).save()

    context['previous_employment_form'] = previous_employment_form

    return render(request, 'wizard.html',context)

@csrf_exempt
@login_required
def confirm(request):
    #previous_employment form

    if request.method == 'GET':
        #import ipdb; ipdb.set_trace()
        context = {'add':True, 'record_added':False, 'form':None}
        form = UserDetailsForm()
        # if request.user.is_authenticated():
        #     username = request.user.username
        user = request.user

        employee = UserDetails.objects.get(employee=user)
        first_name = user.first_name
        last_name = user.last_name
        middle_name = employee.middle_name
        nationality = employee.nationality
        marital_status = employee.marital_status
        wedding_date = employee.wedding_date
        blood_group = employee.blood_group
        land_phone = employee.land_phone
        emergency_phone = employee.emergency_phone
        mobile_phone = employee.mobile_phone
        personal_email = employee.personal_email
        gender = employee.gender

        context = {
        'employee':employee,
        'first_name':first_name,
        'last_name':last_name,
        'middle_name':middle_name,
        'nationality':nationality,
        'marital_status':marital_status,
        'wedding_date':wedding_date,
        'blood_group':blood_group,
        'land_phone':land_phone,
        'emergency_phone':emergency_phone,
        'mobile_phone':mobile_phone,
        'personal_email':personal_email,
        'gender':gender,
        }

        context.update(csrf(request))
#ontext = {'form':form}

        return render(request, 'wizard.html',context)
