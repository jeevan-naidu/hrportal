from django.shortcuts import render, redirect, render_to_response
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from django.views.generic import View
from django.views.generic import CreateView
from django.views.decorators.csrf import csrf_protect
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from models import Address, UserDetails, Education, PreviousEmployment, Proof
from forms import UserDetailsForm, EducationForm, PreviousEmploymentForm, ProofForm, UserRegistrationForm, UserUpdateForm

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

@csrf_protect
@login_required
def user_details(request):
    #import ipdb; ipdb.set_trace()
    # user details form

    context = {"form": ""}
    #username = None
    if request.method == 'GET':
        form = UserDetailsForm(request.POST)
    # if request.user.is_authenticated():
    #     username = request.user.username
    if request.method == 'POST':
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

    context.update(csrf(request))

    context['form'] = form

    return render(request, 'wizard.html',context)

@csrf_protect
@login_required
def user_update_details(request):
    import ipdb; ipdb.set_trace()
    # user Update form

    context = {"form": ""}
    username = None
    if request.method == 'GET':
        form = UserUpdateForm(request.POST)
    # if request.user.is_authenticated():
    #     username = request.user.username
    if request.method == 'POST':
        form = UserUpdateForm(request.POST)
        user = request.user
        if form.is_valid():
            employee = UserDetails.objects.filter(user=user)
            first_name = employee.first_name
            last_name = user.last_name
            middle_name = employee.middle_name
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


    context.update(csrf(request))
    context['form'] = form

    return render_to_response('update.html',context)

@csrf_protect
@login_required
def education(request):
    #import ipdb; ipdb.set_trace()
    #education form
    context = {"education_form": ""}
    username = None
    if request.method == 'GET':
        education_form = EducationForm(request.POST, prefix="education_form")

    if request.method == 'POST':
        education_form = EducationForm(request.POST, prefix="education_form")
        if education_form.is_valid():
            employee = User.objects.get(username=request.user)
            qualification = education_form.cleaned_data['qualification']
            specialization = education_form.cleaned_data['specialization']
            from_date = education_form.cleaned_data['from_date']
            to_date = education_form.cleaned_data['to_date']
            institution = education_form.cleaned_data['institution']
            overall_marks = education_form.cleaned_data['overall_marks']

            Education(employee = employee,
            qualification=qualification,
            specialization=specialization,
            from_date=from_date,
            to_date=to_date,
            institution=institution,
            overall_marks=overall_marks).save()

    context = {}
    context.update(csrf(request))

    context['education_form'] = education_form

    return render_to_response('user_details.html',context)

@csrf_protect
@login_required
def proof(request):
    #import ipdb; ipdb.set_trace()
    #proof form
    context = {"proof_form": ""}
    if request.method == 'GET':
        proof_form = ProofForm(request.GET, prefix="proof_form")
    if request.method == 'POST':
        proof_form = ProofForm(request.POST, prefix="proof_form")
        if proof_form.is_valid():
            employee = User.objects.get(username=request.user)
            pan = proof_form.cleaned_data['pan']
            aadhar_card = proof_form.cleaned_data['aadhar_card']
            dl = proof_form.cleaned_data['dl']
            passport = proof_form.cleaned_data['passport']
            voter_id = proof_form.cleaned_data['voter_id']

            Proof(employee = employee,
            pan=pan,
            aadhar_card=aadhar_card,
            dl=dl,
            passport=passport,
            voter_id=voter_id).save()

    context = {}
    context.update(csrf(request))

    context['proof_form'] = proof_form

    return render_to_response('user_details.html',context)

@csrf_protect
@login_required
def previous_employment(request):
    #import ipdb; ipdb.set_trace()
    #previous_employment form
    context = {"previous_employment_form": ""}
    if request.method == 'GET':
        previous_employment_form = PreviousEmploymentForm(request.GET, prefix="previous_employment_form")
    if request.method == 'POST':
        previous_employment_form = PreviousEmploymentForm(request.POST, prefix="previous_employment_form")
        if previous_employment_form.is_valid():
            employee = User.objects.get(username=request.user)
            company_name = previous_employment_form.cleaned_data['company_name']
            employed_from = previous_employment_form.cleaned_data['employed_from']
            employed_upto = previous_employment_form.cleaned_data['employed_upto']
            pf_number = previous_employment_form.cleaned_data['pf_number']
            last_ctc = previous_employment_form.cleaned_data['last_ctc']
            reason_for_exit = previous_employment_form.cleaned_data['reason_for_exit']

            PreviousEmployment(employee = employee,
            company_name=company_name,
            employed_from=employed_from,
            employed_upto=employed_upto,
            pf_number = pf_number,
            last_ctc=last_ctc,
            reason_for_exit=reason_for_exit).save()

    context = {}
    context.update(csrf(request))

    context['previous_employment_form'] = previous_employment_form

    return render_to_response('user_details.html',context)
