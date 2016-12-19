from django.shortcuts import render, redirect, render_to_response
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.template.loader import render_to_string
from django.contrib import auth
import datetime
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from django.views.generic import View
from django.contrib import messages
from django.views.generic import CreateView
from django.conf import settings
from django.utils import timezone
from django.http import JsonResponse
import random
import string
from django.core.mail import send_mail
from formtools.wizard.views import SessionWizardView
from django.views.decorators.csrf import csrf_protect
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from models import Address, UserDetails, Education, PreviousEmployment, Proof, ConfirmationCode
from forms import UserDetailsForm, EducationForm, PreviousEmploymentForm, ProofForm, UserRegistrationForm

AllowedFileTypes = ['jpg', 'csv','png', 'pdf', 'xlsx', 'xls', 'docx', 'doc', 'jpeg', 'eml']
# Create your views here.
def EmployeeWelcome(request):
    return render(request, 'welcome.html',{})

#@login_required
def login(request):
	context = {}
	context.update(csrf(request))
	return render_to_response('login.html',context)

def auth_view(request):
	username = request.POST.get('username','')
	password = request.POST.get('password','')
	user = auth.authenticate(username=username, password=password)
        userobj = User.objects.get(username=username)

	if user is not None and userobj.is_active is True:
		auth.login(request, user)
		return HttpResponseRedirect('/loggedin')
	else:
		return HttpResponseRedirect('/invalid')

def logout(request):
	auth.logout(request)
	return render_to_response('logout.html')

@login_required
def loggedin(request):
	return render_to_response('loggedin.html',{'user':request.user.username})

def invalid_login(request):
	return render_to_response('invalid.html')

def register(request):
    #import ipdb; ipdb.set_trace()
    if request.method == 'POST':
        # user = request.user
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            password1 = request.POST['password1']
            password2 = request.POST['password2']
            email = request.POST['email']
            
            form.save()
            userobj = User.objects.get(username=username)
            userobj.is_active = 0
            userobj.save()
            send_registration_confirmation(username)
           
            return HttpResponseRedirect('/')
        else:
            print form.is_valid()
            print form['email'].errors
            print form['username'].errors
            print form['password1'].errors
            print form['password2'].errors
    else:
        form = UserRegistrationForm()

    context = {}
    context.update(csrf(request))

    return render(request,'register.html', {'form':form})

def send_registration_confirmation(username):
    # user = request.user
    username = User.objects.get(username=username)
    confirmation_code = ''.join(random.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for x in range(33))
    ccc = ConfirmationCode(confirmation_code=confirmation_code,username=username)
    ccc.save()
    p = ccc
    title = "Thanks for registration"
    content = "http://35.154.44.172:8000/confirmation/" + str(p.confirmation_code) + "/" + username.username
    send_mail(title, content, 'dummy@ansrsource.com', [username.email], fail_silently=False)

def confirmation(request, confirmation_code, username):
    print confirmation_code
    print username
    # import ipdb; ipdb.set_trace()
    try:
        username = User.objects.get(username=username)
        ccc = ConfirmationCode(confirmation_code=confirmation_code,username=username)
        if ccc.confirmation_code == confirmation_code and username.date_joined > timezone.make_aware(datetime.datetime.now()-datetime.timedelta(days=1)):
            username.is_active = True
            username.save()
            username.backend='django.contrib.auth.backends.ModelBackend' 
            auth.login(request,username)
        return HttpResponseRedirect('/user')
    except:
        return HttpResponseRedirect('/register')

def register_success(request):
	return HttpResponseRedirect("/login")

from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
@login_required
def user_details(request):

    # user details form
    if request.method == 'GET':
        context = {"form":""}
        form = UserDetailsForm()
        context["form"] = form
        # import ipdb; ipdb.set_trace()
        user = request.user
        first_name = user.first_name
        last_name = user.last_name
        email=user.email
        try:
            employee = UserDetails.objects.get(employee=request.user)
            # print employee
        except UserDetails.DoesNotExist:
            context = {"form":""}
            form = UserDetailsForm()
            context["form"] = form
            return render(request, "wizard.html", context)

        middle_name = employee.middle_name
        nationality = employee.nationality
        marital_status = employee.marital_status
        wedding_date = employee.wedding_date
        date_of_birth = employee.date_of_birth
        blood_group = employee.blood_group
        land_phone = employee.land_phone
        emergency_phone1 = employee.emergency_phone1
        emergency_phone2 = employee.emergency_phone2
        mobile_phone = employee.mobile_phone
        personal_email = employee.personal_email
        gender = employee.gender
        form = UserDetailsForm(initial = {'first_name':request.user.first_name,'last_name':request.user.last_name,'middle_name':employee.middle_name,
        'nationality':employee.nationality,'marital_status':employee.marital_status,'wedding_date':wedding_date,'date_of_birth':date_of_birth,'blood_group':employee.blood_group,
        'land_phone':employee.land_phone,'emergency_phone1':employee.emergency_phone1,'emergency_phone2':employee.emergency_phone2,'mobile_phone':employee.mobile_phone,
        'personal_email':employee.personal_email,'gender':employee.gender})

        context["form"] = form
        return render(request, "wizard.html", context)

    # instance = UserDetails.objects.get(employee=request.user)
    if request.method == 'POST':
        # import ipdb; ipdb.set_trace()
        context = {"form":""}
        user = request.user

        # employee_g = UserDetails.objects.get(employee=user.id)
        # print employee
        try:
            UserDetails.objects.get(employee=user.id)
            tempsv = UserDetails.objects.get(employee=user.id)
            tempsv.land_phone = None
            tempsv.emergency_phone1 = None
            tempsv.emergency_phone2 = None
            tempsv.mobile_phone = None
            tempsv.save()
        except:
            user = request.user
        form = UserDetailsForm(request.POST)

        if form.is_valid():
            try:
                if UserDetails.objects.get(employee=request.user):
                    user = request.user
                    employee = User.objects.get(username=request.user)
                    first_name = form.cleaned_data['first_name']
                    last_name = form.cleaned_data['last_name']
                    middle_name = form.cleaned_data['middle_name']
                    nationality = form.cleaned_data['nationality']
                    marital_status = form.cleaned_data['marital_status']
                    wedding_date = form.cleaned_data['wedding_date']
                    date_of_birth = form.cleaned_data['date_of_birth']
                    blood_group = form.cleaned_data['blood_group']
                    land_phone = form.cleaned_data['land_phone']
                    emergency_phone1 = form.cleaned_data['emergency_phone1']
                    emergency_phone2 = form.cleaned_data['emergency_phone2']
                    mobile_phone = form.cleaned_data['mobile_phone']
                    personal_email = form.cleaned_data['personal_email']
                    gender = form.cleaned_data['gender']

                    userdata = UserDetails.objects.get(employee=user.id)
                    userdata.first_name = first_name
                    userdata.last_name = last_name
                    userdata.middle_name = middle_name
                    userdata.nationality = nationality
                    userdata.marital_status = marital_status
                    userdata.wedding_date = wedding_date
                    userdata.date_of_birth = date_of_birth
                    userdata.blood_group = blood_group
                    userdata.land_phone = land_phone
                    userdata.emergency_phone1 = emergency_phone1
                    userdata.emergency_phone2 = emergency_phone2
                    userdata.mobile_phone = mobile_phone
                    userdata.personal_email = personal_email
                    userdata.gender = gender
                    userdata.save()

                    """UserDetails(employee = employee_g.employee,
                    middle_name=middle_name,
                    nationality=nationality,
                    marital_status=marital_status,
                    wedding_date=wedding_date,
                    date_of_birth=date_of_birth,
                    blood_group=blood_group,
                    land_phone=land_phone,
                    emergency_phone1=emergency_phone1,
                    emergency_phone2=emergency_phone2,
                    mobile_phone=mobile_phone,
                    personal_email=personal_email,
                    gender=gender).save()"""

                    context['form'] = form
                    return HttpResponseRedirect('/user_details/education')

            except UserDetails.DoesNotExist:
                user = request.user
                employee = User.objects.get(username=request.user)
                #print "laal1"
                first_name = form.cleaned_data['first_name']
                last_name = form.cleaned_data['last_name']
                middle_name = form.cleaned_data['middle_name']
                nationality = form.cleaned_data['nationality']
                marital_status = form.cleaned_data['marital_status']
                wedding_date = form.cleaned_data['wedding_date']
                date_of_birth = form.cleaned_data['date_of_birth']
                blood_group = form.cleaned_data['blood_group']
                land_phone = form.cleaned_data['land_phone']
                emergency_phone1 = form.cleaned_data['emergency_phone1']
                emergency_phone2 = form.cleaned_data['emergency_phone2']
                mobile_phone = form.cleaned_data['mobile_phone']
                personal_email = form.cleaned_data['personal_email']
                gender = form.cleaned_data['gender']

                UserDetails(employee = employee,
                middle_name=middle_name,
                nationality=nationality,
                marital_status=marital_status,
                wedding_date=wedding_date,
                date_of_birth=date_of_birth,
                blood_group=blood_group,
                land_phone=land_phone,
                emergency_phone1=emergency_phone1,
                emergency_phone2=emergency_phone2,
                mobile_phone=mobile_phone,
                personal_email=personal_email,
                gender=gender).save()

                context['form'] = form
                return HttpResponseRedirect('/user_details/education')

    return render(request, 'education.html', context)

@csrf_exempt
@login_required
def education(request):
    #education form
    # import ipdb; ipdb.set_trace()
    if request.method == 'GET':

        context = {"form":""}
        form = EducationForm()
        context["form"] = form
        # import ipdb; ipdb.set_trace()
        user = request.user
        try:
            qualification = request.GET.get('qualification', '')
            specialization = request.GET.get('specialization', '')
            employee = Education.objects.get(employee=request.user,
                    qualification=qualification, specialization=specialization)
            from_date = employee.from_date
            to_date = employee.to_date
            institute = employee.institute
            board_university = employee.board_university
            overall_marks = employee.overall_marks
            marks_card_attachment = employee.marks_card_attachment
            form = EducationForm(initial = {'from_date':employee.from_date,'qualification':employee.qualification,'specialization':employee.specialization,
            'from_date':employee.from_date,'to_date':employee.to_date,'institute':employee.institute,'board_university':employee.board_university,
            'overall_marks':employee.overall_marks,'marks_card_attachment':employee.marks_card_attachment})
            context["form"] = form
            
            return render(request, "education_display.html", context)
        except Education.DoesNotExist:
            context = {"form":""}
            form = EducationForm()
            context["form"] = form
            try:
                employee = Education.objects.filter(employee=request.user)
                no_of_degree = len(employee)
                lists = []
                qual = {'qual':'','spec':''}
                for emp in employee:
                    qual['qual'] = emp.qualification
                    qual['spec'] = emp.specialization
                    lists.append(qual)
                    qual = {'qual':'','spec':''}
                # print lists
                return render(request, "education.html", {'form':form,'education_list':lists,'no_of_degree':no_of_degree,'employee':request.user})
                
            except Education.DoesNotExist:            
                return render(request, "education.html", context)

    if request.method == 'POST':
        # import ipdb; ipdb.set_trace()
        #print request.POST
        
        form = EducationForm(request.POST, request.FILES)
        context = {"form":""}
        marks_card_attachment = request.FILES.get('marks_card_attachment',"")

        if form.is_valid():
            try:
                # Education.objects.get(employee=request.user,qualification=qualification,specialization=specialization)
                user = request.user
                employee = User.objects.get(username=request.user)
                qualification = form.cleaned_data['qualification']
                specialization = form.cleaned_data['specialization']
                from_date = form.cleaned_data['from_date']
                to_date = form.cleaned_data['to_date']
                institute = form.cleaned_data['institute']
                board_university = form.cleaned_data['board_university']
                overall_marks = form.cleaned_data['overall_marks']
                marks_card_attachment = form.cleaned_data['marks_card_attachment']
                if request.FILES.get('marks_card_attachment', ""):
                    form.marks_card_attachment = request.FILES['marks_card_attachment']

                userdata = Education.objects.filter(employee=user.id, qualification=qualification,specialization=specialization)
                
                for details in userdata:

                    details.qualification = qualification
                    details.specialization = specialization
                    details.from_date = from_date
                    details.to_date = to_date
                    details.institute = institute
                    details.board_university = board_university
                    details.overall_marks = overall_marks
                    details.marks_card_attachment = marks_card_attachment
                    details.save()
                    context['form'] = form
                    return render(request, 'education_display.html',context)

            except Education.DoesNotExist:
                user = request.user
                employee = User.objects.get(username=request.user)
                qualification = form.cleaned_data['qualification']
                specialization = form.cleaned_data['specialization']
                from_date = form.cleaned_data['from_date']
                to_date = form.cleaned_data['to_date']
                institute = form.cleaned_data['institute']
                board_university = form.cleaned_data['board_university']
                overall_marks = form.cleaned_data['overall_marks']
                marks_card_attachment = form.cleaned_data['marks_card_attachment']
                if request.FILES.get('marks_card_attachment', ""):
                    form.marks_card_attachment = request.FILES['marks_card_attachment']

                Education(employee=employee,
                qualification=qualification,
                specialization=specialization,
                from_date=from_date,
                to_date=to_date,
                institute=institute,
                board_university=board_university,
                overall_marks=overall_marks,
                marks_card_attachment=marks_card_attachment).save()
                context['form'] = form
                return render(request, 'education.html',context)

    user = request.user
    employee = User.objects.get(username=request.user)
    qualification = form.cleaned_data['qualification']
    specialization = form.cleaned_data['specialization']
    from_date = form.cleaned_data['from_date']
    to_date = form.cleaned_data['to_date']
    institute = form.cleaned_data['institute']
    board_university = form.cleaned_data['board_university']
    overall_marks = form.cleaned_data['overall_marks']
    marks_card_attachment = form.cleaned_data['marks_card_attachment']
    if request.FILES.get('marks_card_attachment', ""):
        form.marks_card_attachment = request.FILES['marks_card_attachment']

    Education(employee=employee,
    qualification=qualification,
    specialization=specialization,
    from_date=from_date,
    to_date=to_date,
    institute=institute,
    board_university=board_university,
    overall_marks=overall_marks,
    marks_card_attachment=marks_card_attachment).save()
    context['form'] = form
    return render(request, 'education.html',context)

@csrf_exempt
@login_required

def proof(request):
    #proof form
    # context = {"form": ""}
    if request.method == 'GET':
        context = {"form":""}
        form = ProofForm()
        context["form"] = form
        # import ipdb; ipdb.set_trace()
        user = request.user
        try:
            employee = Proof.objects.get(employee=request.user)
        except Proof.DoesNotExist:
            context = {"form":""}
            form = ProofForm()
            context["form"] = form
            return render(request, "proof.html", context)

        pan = employee.pan
        pan_attachment = employee.pan_attachment
        aadhar_card = employee.aadhar_card
        aadhar_attachment = employee.aadhar_attachment
        dl = employee.dl
        dl_attachment = employee.dl_attachment
        passport = employee.passport
        passport_attachment = employee.passport_attachment
        voter_id = employee.voter_id
        voter_attachment = employee.voter_attachment

        form = ProofForm(initial = {'pan':employee.pan,'pan_attachment':employee.pan_attachment,
        'aadhar_card':employee.aadhar_card,'aadhar_attachment':employee.aadhar_attachment,'dl':employee.dl,
        'dl_attachment':employee.dl_attachment,'passport':employee.passport,'passport_attachment':employee.passport_attachment,
        'voter_id':employee.voter_id, 'voter_attachment':employee.voter_attachment})

        context["form"] = form
        return render(request, "proof.html", context)

    if request.method == 'POST':
        import ipdb; ipdb.set_trace()
        context = {"form":""}
        user = request.user
        try:
            Proof.objects.get(employee=user.id)
            tempsv = Proof.objects.get(employee=user.id)
            tempsv.pan = None
            tempsv.voter_id = None
            tempsv.aadhar = None
            tempsv.dl = None
            tempsv.passport = None

            tempsv.save()
        except:
            user = request.user
        form = ProofForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                if Proof.objects.get(employee=request.user):
                    user = request.user
                    employee = User.objects.get(username=request.user)
                    pan = form.cleaned_data['pan']
                    pan_attachment = form.cleaned_data['pan_attachment']
                    if request.FILES.get('pan_attachment', ""):
                        form.pan_attachment = request.FILES['pan_attachment']
                    aadhar_card = form.cleaned_data['aadhar_card']
                    aadhar_attachment = form.cleaned_data['aadhar_attachment']
                    if request.FILES.get('aadhar_attachment', ""):
                        form.aadhar_attachment = request.FILES['aadhar_attachment']
                    dl = form.cleaned_data['dl']
                    dl_attachment = form.cleaned_data['dl_attachment']
                    if request.FILES.get('dl_attachment', ""):
                        form.dl_attachment = request.FILES['dl_attachment']
                    passport = form.cleaned_data['passport']
                    passport_attachment = form.cleaned_data['passport_attachment']
                    if request.FILES.get('passport_attachment', ""):
                        form.passport_attachment = request.FILES['passport_attachment']
                    voter_id = form.cleaned_data['voter_id']
                    voter_attachment = form.cleaned_data['voter_attachment']
                    if request.FILES.get('voter_attachment', ""):
                        form.voter_attachment = request.FILES['voter_attachment']

                    fields = [pan,aadhar_card,dl,passport,voter_id]

                    check = [ val for val in fields ]
                    if len(check) > 1:
                        userdata = Proof.objects.get(employee=user.id)
                        userdata.pan = pan
                        userdata.pan_attachment = pan_attachment
                        userdata.aadhar_card = aadhar_card
                        userdata.aadhar_attachment = aadhar_attachment
                        userdata.dl = dl
                        userdata.dl_attachment = dl_attachment
                        userdata.passport = passport
                        userdata.passport_attachment = passport_attachment
                        userdata.voter_id = voter_id
                        userdata.voter_attachment = voter_attachment
                        userdata.save()
                        context['form'] = form

                        return HttpResponseRedirect("/user_details/confirm")
                    else:
                        return HttpResponse("Please fill min 2 fields")

            except Proof.DoesNotExist:

                user = request.user
                employee = User.objects.get(username=request.user)
                pan = form.cleaned_data['pan']
                pan_attachment = form.cleaned_data['pan_attachment']
                if request.FILES.get('pan_attachment', ""):
                    form.pan_attachment = request.FILES['pan_attachment']
                aadhar_card = form.cleaned_data['aadhar_card']
                aadhar_attachment = form.cleaned_data['aadhar_attachment']
                if request.FILES.get('aadhar_attachment', ""):
                    form.aadhar_attachment = request.FILES['aadhar_attachment']
                dl = form.cleaned_data['dl']
                dl_attachment = form.cleaned_data['dl_attachment']
                if request.FILES.get('dl_attachment', ""):
                    form.dl_attachment = request.FILES['dl_attachment']
                passport = form.cleaned_data['passport']
                passport_attachment = form.cleaned_data['passport_attachment']
                if request.FILES.get('passport_attachment', ""):
                    form.passport_attachment = request.FILES['passport_attachment']
                voter_id = form.cleaned_data['voter_id']
                voter_attachment = form.cleaned_data['voter_attachment']
                if request.FILES.get('voter_attachment', ""):
                    form.voter_attachment = request.FILES['voter_attachment']

                fields = [pan,aadhar_card,dl,passport,voter_id]

                check = [ val for val in fields if val]
                if len(check) > 1:
                    Proof(employee=employee,
                    pan=pan,
                    pan_attachment=pan_attachment,
                    aadhar_card=aadhar_card,
                    aadhar_attachment=aadhar_attachment,
                    dl=dl,
                    dl_attachment=dl_attachment,
                    passport=passport,
                    passport_attachment=passport_attachment,
                    voter_id=voter_id,
                    voter_attachment=voter_attachment).save()
                    context['form'] = form

                    return HttpResponseRedirect("/user_details/confirm")
                else:
                    return HttpResponse("Please fill min 2 fields")


    context['form'] = form
    return render(request,'proof.html',context)

@csrf_exempt
@login_required
def previous_employment(request):
    #previous_employment form

    if request.method == 'GET':
        context = {"form":""}
        form = PreviousEmploymentForm()
        context["form"] = form
        # import ipdb; ipdb.set_trace()
        
        user = request.user
        try:
            company_name = request.GET.get('company_name', '')
            employee = PreviousEmployment.objects.get(employee=request.user,company_name=company_name)
            company_name = employee.company_name
            company_address = employee.company_address
            job_type = employee.job_type
            employed_from = employee.employed_from
            employed_upto = employee.employed_upto
            last_ctc = employee.last_ctc
            reason_for_exit = employee.reason_for_exit
            ps_attachment = employee.ps_attachment
            rl_attachment = employee.rl_attachment

            form = PreviousEmploymentForm(initial = {'company_name':employee.company_name,'company_address':employee.company_address,
            'job_type':employee.job_type,'employed_from':employee.employed_from,'employed_upto':employee.employed_upto,
            'last_ctc':employee.last_ctc,'reason_for_exit':employee.reason_for_exit,'ps_attachment':employee.ps_attachment,
            'rl_attachment':employee.rl_attachment})

            context["form"] = form
            return render(request, "previous_display.html", context)
        except PreviousEmployment.DoesNotExist:
            context = {"form":""}
            form = PreviousEmploymentForm()
            context["form"] = form
            try:
                employee = PreviousEmployment.objects.filter(employee=request.user)
                no_of_companies = len(employee)
                lists = []
                company = {'company_name':''}
                for emp in employee:
                    company['company_name'] = emp.company_name
                    
                    lists.append(company)
                    company = {'company_name':''}
                
                return render(request, "previous.html", {'form':form,'employment_list':lists,'employee':request.user})
            except Education.DoesNotExist:            
                return render(request, "previous.html", context_data)
    #     context["form"] = form
    #     return render(request, "previous.html", context)

    if request.method == 'POST':
        # import ipdb; ipdb.set_trace()

        form = PreviousEmploymentForm(request.POST, request.FILES)
        context = {"form":""}
        ps_attachment = request.FILES.get('ps_attachment',"")
        rl_attachment = request.FILES.get('rl_attachment',"")

        if form.is_valid():
            try:
                # PreviousEmployment.objects.get(employee=request.user)
                user = request.user
                employee = User.objects.get(username=request.user)
                company_name = form.cleaned_data['company_name']
                company_address = form.cleaned_data['company_address']
                job_type = form.cleaned_data['job_type']
                employed_from = form.cleaned_data['employed_from']
                employed_upto = form.cleaned_data['employed_upto']
                last_ctc = form.cleaned_data['last_ctc']
                reason_for_exit = form.cleaned_data['reason_for_exit']
                ps_attachment = form.cleaned_data['ps_attachment']
                if request.FILES.get('ps_attachment', ""):
                    form.ps_attachment = request.FILES['ps_attachment']
                rl_attachment = form.cleaned_data['rl_attachment']
                if request.FILES.get('rl_attachment', ""):
                    form.rl_attachment = request.FILES['rl_attachment']

                userdata = PreviousEmployment.objects.filter(employee=user.id, company_name=company_name)
                for details in userdata:
                    details.company_name = company_name
                    details.company_address = company_address
                    details.job_type = job_type
                    details.employed_from = employed_from
                    details.employed_upto = employed_upto
                    details.last_ctc = last_ctc
                    details.reason_for_exit = reason_for_exit
                    details.ps_attachment = ps_attachment
                    details.rl_attachment = rl_attachment
                    details.save()
                    context['form'] = form
                    return render(request, 'previous.html',context)
            except UserDetails.DoesNotExist:
                user = request.user
                employee = User.objects.get(username=request.user)
                company_name = form.cleaned_data['company_name']
                company_address = form.cleaned_data['company_address']
                job_type = form.cleaned_data['job_type']
                employed_from = form.cleaned_data['employed_from']
                employed_upto = form.cleaned_data['employed_upto']
                last_ctc = form.cleaned_data['last_ctc']
                reason_for_exit = form.cleaned_data['reason_for_exit']
                ps_attachment = form.cleaned_data['ps_attachment']
                if request.FILES.get('ps_attachment', ""):
                    form.ps_attachment = request.FILES['ps_attachment']
                rl_attachment = form.cleaned_data['rl_attachment']
                if request.FILES.get('rl_attachment', ""):
                    form.rl_attachment = request.FILES['rl_attachment']

                PreviousEmployment(employee=employee,
                company_name=company_name,
                company_address=company_address,
                job_type=job_type,
                employed_from=employed_from,
                employed_upto=employed_upto,
                last_ctc=last_ctc,
                reason_for_exit=reason_for_exit,
                ps_attachment=ps_attachment,
                rl_attachment=rl_attachment).save()
                context['form'] = form
                return render(request, 'previous.html',context)

    user = request.user
    employee = User.objects.get(username=request.user)
    company_name = form.cleaned_data['company_name']
    company_address = form.cleaned_data['company_address']
    job_type = form.cleaned_data['job_type']
    employed_from = form.cleaned_data['employed_from']
    employed_upto = form.cleaned_data['employed_upto']
    last_ctc = form.cleaned_data['last_ctc']
    reason_for_exit = form.cleaned_data['reason_for_exit']
    ps_attachment = form.cleaned_data['ps_attachment']
    if request.FILES.get('ps_attachment', ""):
        form.ps_attachment = request.FILES['ps_attachment']
    rl_attachment = form.cleaned_data['rl_attachment']
    if request.FILES.get('rl_attachment', ""):
        form.rl_attachment = request.FILES['rl_attachment']

    PreviousEmployment(employee=employee,
    company_name=company_name,
    company_address=company_address,
    job_type=job_type,
    employed_from=employed_from,
    employed_upto=employed_upto,
    last_ctc=last_ctc,
    reason_for_exit=reason_for_exit,
    ps_attachment=ps_attachment,
    rl_attachment=rl_attachment).save()
    context['form'] = form
    return render(request, 'previous.html',context)

@csrf_exempt
@login_required
def confirm(request):
    
    if request.user.is_authenticated:

        if request.method == 'GET':
            context = {'add':True, 'record_added':False, 'form':None}
            form = UserDetailsForm()
            user = request.user
            try:
                employee = UserDetails.objects.get(employee=request.user)
            except UserDetails.DoesNotExist:
                return HttpResponseRedirect('/user_details')

            first_name = user.first_name
            last_name = user.last_name
            middle_name = employee.middle_name
            nationality = employee.nationality
            marital_status = employee.marital_status
            wedding_date = employee.wedding_date
            blood_group = employee.blood_group
            land_phone = employee.land_phone
            emergency_phone1 = employee.emergency_phone1
            emergency_phone2 = employee.emergency_phone2
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
            'emergency_phone1':emergency_phone1,
            'emergency_phone2':emergency_phone2,
            'mobile_phone':mobile_phone,
            'personal_email':personal_email,
            'gender':gender,
            }

            context.update(csrf(request))

            return render(request, 'confirm.html',context)
    else:
        return HttpResponseRedirect('/login')

def download_form(request):
    return render(request, 'download_forms.html',{})
