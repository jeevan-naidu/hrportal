from django.shortcuts import render, redirect, render_to_response
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.template.loader import render_to_string
from django.contrib import auth
import datetime
from django.contrib.auth.decorators import login_required
from django.template.context_processors import csrf
from django.views.generic import View
from django.contrib import messages
from django.views.generic import CreateView
from django.conf import settings
from django.utils import timezone
from django.http import JsonResponse
import random
import string
from axes.decorators import watch_login
from axes.utils import reset
from django.contrib import messages
from django.core.mail import send_mail
from formtools.wizard.views import SessionWizardView
from django.views.decorators.csrf import csrf_protect
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from models import Address, UserDetails, Education, PreviousEmployment, Proof, ConfirmationCode, FamilyDetails, LanguageProficiency,EducationUniversity, EducationSpecialization, EducationInstitute
from forms import UserDetailsForm, EducationForm, PreviousEmploymentForm, ProofForm, UserRegistrationForm, FamilyDetailsForm, LanguageProficiencyForm 

AllowedFileTypes = ['jpg', 'csv','png', 'pdf', 'xlsx', 'xls', 'docx', 'doc', 'jpeg', 'eml']
# Create your views here.
def EmployeeWelcome(request):
    return render(request, 'welcome.html',{})

#@login_required
@watch_login
def login(request):
    context = {}
    context.update(csrf(request))
    return render_to_response('login.html',context)

@watch_login
def auth_view(request):
    username = request.POST.get('username','')
    password = request.POST.get('password','')
    # import ipdb; ipdb.set_trace()

    user = auth.authenticate(username=username, password=password)
    try:
        userobj = User.objects.get(username=username)
    except User.DoesNotExist:
        messages.error(request, 'Please register and confirm from your email to login')
        return render(request,'login.html')       
    if user is not None and userobj.is_active is True:
        auth.login(request, user)
        return HttpResponseRedirect('/loggedin')
    else:
        messages.error(request, 'Invalid Username or password')
        return render(request,'login.html')

def logout(request):
    auth.logout(request)
    return render_to_response('logout.html')

@login_required
def loggedin(request):
    return render(request,'loggedin.html',{'user':request.user.username})

def invalid_login(request):
    return render_to_response('invalid.html')

def register(request):
    # import ipdb; ipdb.set_trace()
    if request.method == 'POST':
        # user = request.user
        context = {"form":""}
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
            messages.error(request, 'Please check your email and click the given link')
            context["form"] = form
            return render(request,'welcome.html', context)
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
    send_mail(title, content, 'myansrsource@ansrsource.com', [username.email], fail_silently=False)

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
        context = {"form":"", "language_form":""}
        form = UserDetailsForm(request.FILES)
        lang_form = LanguageProficiencyForm()
        context["form"] = form
        # import ipdb; ipdb.set_trace()
        user = request.user
        first_name = user.first_name
        last_name = user.last_name
        email=user.email
        try:
            employee = UserDetails.objects.get(employee=request.user)
            employee_lang = LanguageProficiency.objects.get(employee=request.user)
            
            try:
                address_type = request.GET.get('address_type','')
                address = Address.objects.get(employee=request.user, address_type=address_type)
                form = UserDetailsForm(initial = {'name_pan':employee.name_pan,'photo':employee.photo,
                'nationality':employee.nationality,'date_of_birth':employee.date_of_birth,'blood_group':employee.blood_group,
                'land_phone':employee.land_phone,'mobile_phone':employee.mobile_phone,'gender':employee.gender,
                'address_type':address.address_type,'address1':address.address1,'address2':address.address2,
                'city':address.city,'state':address.state,'zipcode':address.zipcode})

                lang_form = LanguageProficiencyForm(initial = {'language_known':employee_lang.language_known,'speak':employee_lang.speak,
                'read':employee_lang.read,'write':employee_lang.write})

                context["form"] = form
                context["lang_form"] = lang_form                

                return render(request, "form_templates/user_profile.html", context)
                try:
                    address_type = request.GET.get('address_type','')
                    address = Address.objects.get(employee=request.user, address_type=address_type)

                    form = UserDetailsForm(initial = {'name_pan':employee.name_pan,'photo':employee.photo,
                    'nationality':employee.nationality,'date_of_birth':employee.date_of_birth,
                    'blood_group':employee.blood_group,'land_phone':employee.land_phone,
                    'mobile_phone':employee.mobile_phone,'gender':employee.gender,'address_type':address.address_type,
                    'address1':address.address1,'address2':address.address2,'city':address.city,'state':address.state,
                    'zipcode':address.zipcode})
                    form = LanguageProficiencyForm(initial = {'language_known':employee_lang.language_known,'speak':employee_lang.speak,
                    'read':employee_lang.read,'write':employee_lang.write})
                    context["form"] = form
                    context["lang_form"] = lang_form
                    return render(request, "form_templates/user_profile.html", context)

                except Address.DoesNotExist:
                    
                    form = UserDetailsForm(initial = {'name_pan':employee.name_pan,'photo':employee.photo,
                    'nationality':employee.nationality,'date_of_birth':employee.date_of_birth,
                    'blood_group':employee.blood_group,'land_phone':employee.land_phone,
                    'mobile_phone':employee.mobile_phone,'gender':employee.gender})
                    try:
                        address = Address.objects.get(employee=request.user,address_type='PR')
                        employee = Address.objects.filter(employee=request.user)
                        no_of_degree = len(employee)
                        lists = []
                        addre = {'address_type':''}
                        for emp in employee:
                            addre['address_type'] = emp.address_type
                            
                            lists.append(addre)
                            addre = {'address_type':''}

                        # print lists
                        return render(request, "form_templates/user_profile.html", {'form':form,'address_list':lists,'no_of_degree':no_of_degree,
                            'employee':request.user})
                    
                    except Address.DoesNotExist:            
                        return render(request, "form_templates/user_profile.html", context)

            except Address.DoesNotExist:
                try:

                    address = Address.objects.get(employee=request.user, address_type='PR')
                    photo = employee.photo
                    form = UserDetailsForm(initial = {'name_pan':employee.name_pan,'photo':employee.photo,
                    'nationality':employee.nationality,'date_of_birth':employee.date_of_birth,'blood_group':employee.blood_group,
                    'land_phone':employee.land_phone,'mobile_phone':employee.mobile_phone,'gender':employee.gender,
                    'address_type':address.address_type,'address1':address.address1,'address2':address.address2,
                    'city':address.city,'state':address.state,'zipcode':address.zipcode})
                    lang_form = LanguageProficiencyForm(initial = {'language_known':employee_lang.language_known,'speak':employee_lang.speak,
                        'read':employee_lang.read,'write':employee_lang.write})
                    

                    context["form"] = form
                    context["lang_form"] = lang_form
                    return render(request, "form_templates/user_profile.html", context)

                except Address.DoesNotExist:

                    address = Address.objects.get(employee=request.user, address_type='TM')
                    photo = employee.photo
                    form = UserDetailsForm(initial = {'name_pan':employee.name_pan,'photo':employee.photo,
                    'nationality':employee.nationality,'date_of_birth':employee.date_of_birth,'blood_group':employee.blood_group,
                    'land_phone':employee.land_phone,'mobile_phone':employee.mobile_phone,'gender':employee.gender,
                    'address_type':address.address_type,'address1':address.address1,'address2':address.address2,
                    'city':address.city,'state':address.state,'zipcode':address.zipcode})
                    lang_form = LanguageProficiencyForm(initial = {'language_known':employee_lang.language_known,'speak':employee_lang.speak,
                        'read':employee_lang.read,'write':employee_lang.write})
                    

                    context["form"] = form
                    context["lang_form"] = lang_form
                    return render(request, "form_templates/user_profile.html", context)
            # print employee
        except UserDetails.DoesNotExist:
            context = {"form":""}
            form = UserDetailsForm(request.FILES)
            lang_form = LanguageProficiencyForm()
            
            context["form"] = form
            context["lang_form"] = lang_form
            return render(request, "form_templates/user_profile.html", context)

    # instance = UserDetails.objects.get(employee=request.user)
    if request.method == 'POST':
        import ipdb; ipdb.set_trace()
        context = {"form":""}
        user = request.user

        try:
            UserDetails.objects.get(employee=user.id)
            tempsv = UserDetails.objects.get(employee=user.id)
            tempsv.land_phone = None
            tempsv.mobile_phone = None
            tempsv.save()
        except:
            user = request.user
        form = UserDetailsForm(request.POST, request.FILES)
        lang_form = LanguageProficiencyForm(request.POST)

        if form.is_valid():
            try:
                if UserDetails.objects.get(employee=request.user):
                    user = request.user
                    employee = UserDetails.objects.get(employee=request.user)
                
                    photo = form.cleaned_data['photo']
                    if request.FILES.get('photo', ""):
                        form.photo = request.FILES['photo']
                     
                    name_pan = form.cleaned_data['name_pan']
                    nationality = form.cleaned_data['nationality']
                    date_of_birth = form.cleaned_data['date_of_birth']
                    blood_group = form.cleaned_data['blood_group']
                    land_phone = form.cleaned_data['land_phone']
                    mobile_phone = form.cleaned_data['mobile_phone']
                    gender = form.cleaned_data['gender']
                    address_type = form.cleaned_data['address_type']
                    address1 = form.cleaned_data['address1']
                    address2 = form.cleaned_data['address2']
                    city = form.cleaned_data['city']
                    state = form.cleaned_data['state']
                    zipcode = form.cleaned_data['zipcode']

                    userdata = UserDetails.objects.get(employee=user.id)
                    try:
                        userdata1 = Address.objects.get(employee=user.id, address_type='PR')
                        
                        userdata.name_pan = name_pan
                        userdata.photo = photo
                        userdata.nationality = nationality
                        userdata.date_of_birth = date_of_birth
                        userdata.blood_group = blood_group
                        userdata.land_phone = land_phone
                        userdata.mobile_phone = mobile_phone
                        userdata.gender = gender
                        userdata1.address_type=address_type
                        userdata1.address1=address1
                        userdata1.address2=address2
                        userdata1.city=city
                        userdata1.state=state
                        userdata1.zipcode=zipcode
                        try:
                            userdata.save()
                        except Exception,e:
                            print str(e)
                        userdata1.save()
                        
                        context['form'] = form
                        return HttpResponseRedirect('/user_details/education')

                    except Address.DoesNotExist:
                        userdata1 = Address.objects.get(employee=user.id, address_type='TM')
                        
                        userdata.name_pan = name_pan
                        userdata.photo = photo
                        userdata.nationality = nationality
                        userdata.date_of_birth = date_of_birth
                        userdata.blood_group = blood_group
                        userdata.land_phone = land_phone
                        userdata.mobile_phone = mobile_phone
                        userdata.gender = gender
                        userdata1.address_type=address_type
                        userdata1.address1=address1
                        userdata1.address2=address2
                        userdata1.city=city
                        userdata1.state=state
                        userdata1.zipcode=zipcode
                        try:
                            userdata.save()
                        except Exception,e:
                            print str(e)
                        userdata1.save()
                        
                        context['form'] = form
                        return HttpResponseRedirect('/user_details/education')

            except UserDetails.DoesNotExist:
                user = request.user
                employee = User.objects.get(username=request.user)
                #print "laal1"
                name_pan = form.cleaned_data['name_pan']
                photo = form.cleaned_data['photo']
                if request.FILES.get('photo', ""):
                    form.photo = request.FILES['photo']
                nationality = form.cleaned_data['nationality']
                date_of_birth = form.cleaned_data['date_of_birth']
                blood_group = form.cleaned_data['blood_group']
                land_phone = form.cleaned_data['land_phone']
                mobile_phone = form.cleaned_data['mobile_phone']
                gender = form.cleaned_data['gender']
                address = User.objects.get(username=request.user)
                address_type = form.cleaned_data['address_type']
                address1 = form.cleaned_data['address1']
                address2 = form.cleaned_data['address2']
                city = form.cleaned_data['city']
                state = form.cleaned_data['state']
                zipcode = form.cleaned_data['zipcode']
                language_known = lang_form.cleaned_data['language_known']
                speak = lang_form.cleaned_data['speak']
                read = lang_form.cleaned_data['read']
                write = lang_form.cleaned_data['write']
                
                UserDetails(employee = employee,name_pan=name_pan,photo=photo,nationality=nationality,
                date_of_birth=date_of_birth,blood_group=blood_group,land_phone=land_phone,
                mobile_phone=mobile_phone,gender=gender).save()
                print employee
                Address(employee=employee, address_type=address_type,address1=address1,address2=address2,
                    city=city,state=state,zipcode=zipcode).save()
                LanguageProficiency(employee=employee, language_known=language_known,speak=speak,read=read,write=write).save()

                context['form'] = form
                return HttpResponseRedirect('/user_details/education')

        else:
            
            print form.is_valid()
            # import ipdb; ipdb.set_trace()
            name_pan_errors = form['name_pan'].errors
            nationality_errors = form['nationality'].errors
            date_of_birth_errors = form['date_of_birth'].errors
            blood_group_errors = form['blood_group'].errors
            land_phone_errors = form['land_phone'].errors
            mobile_phone_errors = form['mobile_phone'].errors
            gender_errors = form['gender'].errors
            address_type_errors = form['address_type'].errors
            address1_errors = form['address1'].errors
            address2_errors = form['address2'].errors
            city_errors = form['city'].errors
            state_errors = form['state'].errors
            zipcode_errors = form['zipcode'].errors
            
            return render(request, 'form_templates/user_profile.html', {'form':form, 'name_pan_errors':name_pan_errors,
            'nationality_errors':nationality_errors,'date_of_birth_errors':date_of_birth_errors,'blood_group_errors':blood_group_errors,
            'land_phone_errors':land_phone_errors,'mobile_phone_errors':mobile_phone_errors,'gender_errors':gender_errors,
            'address_type_errors':address_type_errors,'address1_errors':address1_errors,'address2_errors':address2_errors,
            'city_errors':city_errors,'state_errors':state_errors,'zipcode_errors':zipcode_errors})

    return render(request, 'form_templates/education.html', context)

@login_required
def family_details(request):
    if request.method == 'GET':
        context = {"form":""}
        form = FamilyDetailsForm()
        context["form"] = form
        # import ipdb; ipdb.set_trace()
        try:
            employee = FamilyDetails.objects.get(employee=request.user)
            
            form = FamilyDetailsForm(initial = {'marital_status':employee.marital_status,'wedding_date':employee.wedding_date,
            'spouse_name':employee.spouse_name,'no_of_children':employee.no_of_children,'mother_name':employee.mother_name,
            'mother_dob':employee.mother_dob,'mother_profession':employee.mother_profession,'father_name':employee.father_name,
            'father_dob':employee.father_dob,'father_profession':employee.father_profession,'emergency_phone1':employee.emergency_phone1,
            'emergency_phone2':employee.emergency_phone2,'child1_name':employee.child1_name,'child2_name':employee.child2_name})

            context["form"] = form
            return render(request, "form_templates/family_details.html", context)
            # print employee
        except FamilyDetails.DoesNotExist:
            context = {"form":""}
            form = FamilyDetailsForm()
            context["form"] = form
            return render(request, "form_templates/family_details.html", context)
    
    if request.method == 'POST':
        # import ipdb; ipdb.set_trace()
        context = {"form":""}
        user = request.user
        try:
            FamilyDetails.objects.get(employee=user.id)
            tempsv = FamilyDetails.objects.get(employee=user.id)
            tempsv.emergency_phone2 = None
            tempsv.emergency_phone1 = None
            tempsv.save()
        except:
            user = request.user
        form = FamilyDetailsForm(request.POST)

        if form.is_valid():
            try:
                if FamilyDetails.objects.get(employee=request.user):
                    user = request.user
                    employee = User.objects.get(username=request.user)
                    marital_status = form.cleaned_data['marital_status']
                    wedding_date = form.cleaned_data['wedding_date']
                    spouse_name = form.cleaned_data['spouse_name']
                    no_of_children = form.cleaned_data['no_of_children']
                    mother_name = form.cleaned_data['mother_name']
                    mother_dob = form.cleaned_data['mother_dob']
                    mother_profession = form.cleaned_data['mother_profession']
                    father_name = form.cleaned_data['father_name']
                    father_dob = form.cleaned_data['father_dob']
                    father_profession = form.cleaned_data['father_profession']
                    emergency_phone1 = form.cleaned_data['emergency_phone1']
                    emergency_phone2 = form.cleaned_data['emergency_phone2']
                    child1_name = form.cleaned_data['child1_name']
                    child2_name = form.cleaned_data['child2_name']
                    
                    userdata = FamilyDetails.objects.get(employee=user.id)
                    
                    userdata.marital_status = marital_status
                    userdata.wedding_date = wedding_date
                    userdata.spouse_name = spouse_name
                    userdata.no_of_children = no_of_children
                    userdata.mother_name = mother_name
                    userdata.mother_profession = mother_profession
                    userdata.mother_dob = mother_dob
                    userdata.father_name = father_name
                    userdata.father_dob = father_dob
                    userdata.father_profession = father_profession
                    userdata.emergency_phone1 = emergency_phone1
                    userdata.emergency_phone2 = emergency_phone2
                    userdata.child1_name=child1_name
                    userdata.child2_name=child2_name
                    try:
                        userdata.save()
                    except Exception,e:
                        print str(e)
                    
                    context['form'] = form
                    return HttpResponseRedirect('/user_details/education')
                    

            except FamilyDetails.DoesNotExist:
                user = request.user
                employee = User.objects.get(username=request.user)
                marital_status = form.cleaned_data['marital_status']
                wedding_date = form.cleaned_data['wedding_date']
                spouse_name = form.cleaned_data['spouse_name']
                no_of_children = form.cleaned_data['no_of_children']
                mother_name = form.cleaned_data['mother_name']
                mother_dob = form.cleaned_data['mother_dob']
                mother_profession = form.cleaned_data['mother_profession']
                father_name = form.cleaned_data['father_name']
                father_dob = form.cleaned_data['father_dob']
                father_profession = form.cleaned_data['father_profession']
                emergency_phone1 = form.cleaned_data['emergency_phone1']
                emergency_phone2 = form.cleaned_data['emergency_phone2']
                child1_name = form.cleaned_data['child1_name']
                child2_name = form.cleaned_data['child2_name']
                
                FamilyDetails(employee = employee,marital_status=marital_status,wedding_date=wedding_date,spouse_name=spouse_name,
                    no_of_children=no_of_children,mother_name=mother_name, mother_dob=mother_dob,mother_profession=mother_profession,
                    father_name=father_name,father_profession=father_profession,father_dob=father_dob, emergency_phone1=emergency_phone1,
                    emergency_phone2=emergency_phone2,child1_name=child1_name,child2_name=child2_name).save()
                print employee
                
                context['form'] = form
                return HttpResponseRedirect('/user_details/education')
        else:
            
            print form.is_valid()
            # import ipdb; ipdb.set_trace()
            marital_status_errors = form['marital_status'].errors
            wedding_date_errors = form['wedding_date'].errors
            spouse_name_errors = form['spouse_name'].errors
            no_of_children_errors = form['no_of_children'].errors
            mother_name_errors = form['mother_name'].errors
            mother_dob_errors = form['mother_dob'].errors
            mother_profession_errors = form['mother_profession'].errors
            father_name_errors = form['father_name'].errors
            father_dob_errors = form['father_dob'].errors
            father_profession_errors = form['father_profession'].errors
            emergency_phone1_errors = form['emergency_phone1'].errors
            emergency_phone2_errors = form['emergency_phone2'].errors
            child1_name_errors = form['child1_name'].errors
            child2_name_errors = form['child2_name'].errors
            
            return render(request, 'form_templates/family_details.html', {'form':form, 'marital_status_errors':marital_status_errors,
            'wedding_date_errors':wedding_date_errors,'spouse_name_errors':spouse_name_errors,'no_of_children_errors':no_of_children_errors,
            'mother_name_errors':mother_name_errors,'mother_dob_errors':mother_dob_errors,'mother_profession_errors':mother_profession_errors,
            'father_name_errors':father_name_errors,'father_dob_errors':father_dob_errors,'father_profession_errors':father_profession_errors,
            'emergency_phone1_errors':emergency_phone1_errors,'emergency_phone2_errors':emergency_phone2_errors,'child1_name_errors':child1_name_errors,
            'child2_name_errors':child2_name_errors})

    return render(request, 'form_templates/education.html', context)

def previous_delete(request):
    
    # import ipdb; ipdb.set_trace()
    if request.method == 'GET':

        
        user = request.user
        company_name = request.GET.get('company_name', '')
        employee = PreviousEmployment.objects.filter(employee=request.user,company_name=company_name).delete()
        context = {"form":""}
        form = PreviousEmploymentForm(request.FILES)
        context["form"] = form
        
        return render(request, "form_templates/previous_display.html", context)

def education_delete(request):
    #education form
    # import ipdb; ipdb.set_trace()
    if request.method == 'GET':

        
        user = request.user
        qualification = request.GET.get('qualification', '')
        specialization = request.GET.get('specialization', '')
        employee = Education.objects.filter(employee=request.user,
            qualification=qualification, specialization=specialization).delete()
        context = {"form":""}
        form = EducationForm(request.FILES)
        context["form"] = form
        
          
        return render(request, "form_templates/education_display.html", context)
        #return HttpResponseRedirect('/user_details/education')

def address_tempo(request):
    # import ipdb; ipdb.set_trace()
    if request.method=='GET':
        context = {"form":""}
        form = UserDetailsForm()
       
        user = request.user
        try:
            employee = UserDetails.objects.get(employee=request.user)

            form = UserDetailsForm(initial = {'name_pan':employee.name_pan,
            'nationality':employee.nationality,'date_of_birth':employee.date_of_birth,
            'blood_group':employee.blood_group,'land_phone':employee.land_phone,
            'mobile_phone':employee.mobile_phone,'gender':employee.gender})
        
            messages.warning(request,"please fill only temporary address here")
            context["form"] = form
            return render(request, "address_tempo.html", context)
        except UserDetails.DoesNotExist:
            context = {"form":""}
            form = UserDetailsForm()
            context["form"] = form
            return HttpResponseRedirect('/user_details')

    if request.method=='POST':
        context = {"form":""}
        
        # form = UserDetailsForm(request.POST)  
        user = request.user      
        employee = UserDetails.objects.get(employee=request.user)

        form = UserDetailsForm(initial = {'name_pan':employee.name_pan,
        'nationality':employee.nationality,'date_of_birth':employee.date_of_birth,
        'blood_group':employee.blood_group,'land_phone':employee.land_phone,
        'mobile_phone':employee.mobile_phone,'gender':employee.gender})
        context = {"form":""}
        form = UserDetailsForm(request.POST)
        
        if form.is_valid():
            address = Address.objects.get(employee=request.user, address_type='PR')
            address_type = 'TM'
            address1 = form.cleaned_data['address1']
            address2 = form.cleaned_data['address2']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            Address(employee=user, address_type=address_type,address1=address1,address2=address2,city=city,state=state,zipcode=zipcode).save()
            context["form"] = form
            return render(request, "address_tempo.html", context)
        else:
            
            messages.error(request, 'Fill the permanent address before copying that to temporary address')
            context["form"] = form
            return render(request,'address_tempo.html', context)
@csrf_exempt
def address_copy(request):
    # import ipdb; ipdb.set_trace()
    if request.method=='POST':
        context = {"form":""}
        
        # form = UserDetailsForm(request.POST)  
        user = request.user
        form = UserDetailsForm(request.POST)
   
        a = request.POST.get('address_type')
        b = request.POST.get('address1')
        C = request.POST.get('address2')
        d = request.POST.get('city')
        e = request.POST.get('state')
        f = request.POST.get('zipcode')
        address = Address.objects.filter(employee=request.user, address_type=a)
        address_type = 'TM'
        address1 = b
        address2 = C
        city = d
        state = e
        zipcode = f

        Address(employee=user, address_type=address_type,address1=address1,address2=address2,city=city,state=state,zipcode=zipcode).save()
        context["form"] = form
        return render(request, "form_templates/user_profile.html", context,{'address_type':address_type,'address1':address1,'address2':address2,'city':city,'state':state,'zipcode':zipcode})

    if request.method=='GET':
        context = {"form":""}
        form = UserDetailsForm()
        messages.error(request, 'Fill the permanent address before copying that to temporary address')
        context["form"] = form
        return render(request,'form_templates/user_profile.html', context)

def checkbox_check(request):

    id = request.GET['id']

    employee = Address.objects.filter(employee = id, address_type='TM')

    if employee:
        valid = True
    else:
        valid = False

    return HttpResponse(valid) 

@login_required
def education(request):
    #education form
    # import ipdb; ipdb.set_trace()
    if request.method == 'GET':

        context = {"form":""}
        form = EducationForm(request.FILES)
        context["form"] = form
        # import ipdb; ipdb.set_trace()
        user = request.user
        try:
            qualification = request.GET.get('qualification', '')
            specialization = request.GET.get('specialization', '')
            employee = Education.objects.get(employee=request.user,
                    qualification=qualification, specialization=specialization)
            
            form = EducationForm(initial = {'education_type':employee.education_type,'from_date':employee.from_date,
            'qualification':employee.qualification,'specialization':employee.specialization,
            'to_date':employee.to_date,'institute':employee.institute,'board_university':employee.board_university,
            'overall_marks':employee.overall_marks,'marks_card_attachment':employee.marks_card_attachment})
            context["form"] = form
            
            return render(request, "form_templates/education_display.html", context)
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
                return render(request, "form_templates/education.html", {'form':form,'education_list':lists,'no_of_degree':no_of_degree,'employee':request.user})
                
            except Education.DoesNotExist:            
                return render(request, "form_templates/education.html", context)

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

                qualification = form.cleaned_data['qualification']
                specialization = form.cleaned_data['specialization']
                employee = Education.objects.get(employee=request.user,qualification=qualification,specialization=specialization)

                education_type = form.cleaned_data['education_type']
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
                    details.education_type = education_type
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
                    return render(request, 'form_templates/education_display.html',context)

            except Education.DoesNotExist:
                user = request.user
                employee = User.objects.get(username=request.user)
                qualification = form.cleaned_data['qualification']
                specialization = form.cleaned_data['specialization']
                education_type = form.cleaned_data['education_type']
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
                education_type=education_type,
                from_date=from_date,
                to_date=to_date,
                institute=institute,
                board_university=board_university,
                overall_marks=overall_marks,
                marks_card_attachment=marks_card_attachment).save()
                context['form'] = form
                return render(request, 'form_templates/education.html',context)

        else:
            print form.is_valid()
            # import ipdb; ipdb.set_trace()
            education_type_errors = form['education_type'].errors
            qualification_errors = form['qualification'].errors
            specialization_errors = form['specialization'].errors
            from_date_errors = form['from_date'].errors
            to_date_errors = form['to_date'].errors
            institute_errors = form['institute'].errors
            board_university_errors = form['board_university'].errors
            overall_marks_errors = form['overall_marks'].errors
            
            return render(request, 'form_templates/education.html', {'form':form, 'education_type_errors':education_type_errors,
            'qualification_errors':qualification_errors,'specialization_errors':specialization_errors,'overall_marks_errors':overall_marks_errors,
            'from_date_errors':from_date_errors,'to_date_errors':to_date_errors,'institute_errors':institute_errors,
            'board_university_errors':board_university_errors})

    user = request.user
    employee = User.objects.get(username=request.user)
    qualification = form.cleaned_data['qualification']
    specialization = form.cleaned_data['specialization']
    education_type = form.cleaned_data['education_type']
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
    education_type=education_type,
    from_date=from_date,
    to_date=to_date,
    institute=institute,
    board_university=board_university,
    overall_marks=overall_marks,
    marks_card_attachment=marks_card_attachment).save()
    context['form'] = form
    return render(request, 'form_templates/education.html',context)


@login_required

def proof(request):
    #proof form
    # context = {"form": ""}
    if request.method == 'GET':
        context = {"form":""}
        form = ProofForm(request.FILES)
        context["form"] = form
        # import ipdb; ipdb.set_trace()
        user = request.user
        try:
            employee = Proof.objects.get(employee=request.user)
        except Proof.DoesNotExist:
            context = {"form":""}
            form = ProofForm(request.FILES)
            context["form"] = form
            return render(request, "form_templates/proof.html", context)

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
        return render(request, "form_templates/proof.html", context)

    if request.method == 'POST':
        # import ipdb; ipdb.set_trace()
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
                    employee = Proof.objects.get(employee=request.user)
                    pan = form.cleaned_data['pan']
                    
                    pan_attachment = form.cleaned_data['pan_attachment']
                    if request.FILES.get('pan_attachment', ""):
                        form.pan_attachment = request.FILES['pan_attachment']
                    
                    aadhar_card = form.cleaned_data['aadhar_card']
                    
                    aadhar_attachment = form.cleaned_data['aadhar_attachment']
                    if request.FILES.get('pan_attachment', ""):
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
                    

                    fields = [pan,aadhar_card, dl, passport, voter_id]

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
                        messages.error(request, 'Please enter min 2 proofs with attachments')
                        context['form'] = form
                        return render(request,'form_templates/proof.html',context)

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
      
                fields = [pan, aadhar_card, dl, passport, voter_id]
                
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
                    messages.error(request, 'Proof details are added successfully')
                    context['form'] = form

                    return HttpResponseRedirect("/user_details/confirm")
                else:
                    messages.error(request, 'Please enter min 2 proofs with attachments')
                    context['form'] = form
                    return render(request,'form_templates/proof.html',context)

        else:
            print form.is_valid()
            # import ipdb; ipdb.set_trace()
            pan_error = form['pan'].errors
            pan_att_error = form['pan_attachment'].errors
            aadhar_error = form['aadhar_card'].errors
            addhar_att_error = form['aadhar_attachment'].errors
            dl_error = form['dl'].errors
            dl_att_error = form['dl_attachment'].errors
            passport_error = form['passport'].errors
            pp_att_error = form['passport_attachment'].errors
            voter_error = form['voter_id'].errors
            voter_att_error =  form['voter_attachment'].errors
            
            return render(request, 'form_templates/proof.html', {'form':form, 'pan_error':pan_error,'pan_att_error':pan_att_error,'aadhar_error':aadhar_error,'addhar_att_error':
            addhar_att_error,'dl_error':dl_att_error,'passport_error':passport_error,'pp_att_error':pp_att_error,'voter_error':voter_error,
            'voter_att_error':voter_att_error })

@csrf_exempt
@login_required
def previous_employment(request):
    #previous_employment form

    if request.method == 'GET':
        context = {"form":""}
        form = PreviousEmploymentForm(request.FILES)
        context["form"] = form
        # import ipdb; ipdb.set_trace()
        
        user = request.user
        try:
            company_name = request.GET.get('company_name', '')
            employee = PreviousEmployment.objects.get(employee=request.user,company_name=company_name)

            form = PreviousEmploymentForm(initial = {'company_name':employee.company_name,'company_address':employee.company_address,
                'job_type':employee.job_type,'employed_from':employee.employed_from,'employed_upto':employee.employed_upto,
                'last_ctc':employee.last_ctc,'reason_for_exit':employee.reason_for_exit,'ps_attachment':employee.ps_attachment,
                'rl_attachment':employee.rl_attachment,'offer_letter_attachment':employee.offer_letter_attachment})

            context["form"] = form

            return render(request, "form_templates/previous_display.html", context)
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
                
                return render(request, "form_templates/previous.html", {'form':form,'employment_list':lists,'employee':request.user})
            except Education.DoesNotExist:            
                return render(request, "form_templates/previous.html", context_data)
    #     context["form"] = form
    #     return render(request, "form_templates/previous.html", context)

    if request.method == 'POST':
        # import ipdb; ipdb.set_trace()

        form = PreviousEmploymentForm(request.POST, request.FILES)
        context = {"form":""}
        ps_attachment = request.FILES.get('ps_attachment',"")
        rl_attachment = request.FILES.get('rl_attachment',"")
        offer_letter_attachment = request.FILES.get('offer_letter_attachment',"")

        if form.is_valid():
            try:
                # PreviousEmployment.objects.get(employee=request.user)
                user = request.user
                employee = PreviousEmployment.objects.get(employee=request.user)
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
                
                offer_letter_attachment = form.cleaned_data['offer_letter_attachment']
                if request.FILES.get('offer_letter_attachment', ""):
                    form.offer_letter_attachment = request.FILES['offer_letter_attachment']
                

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
                    details.offer_letter_attachment = offer_letter_attachment
                    
                    details.save()
                    context['form'] = form
                    return render(request, 'form_templates/previous.html',context)
            except PreviousEmployment.DoesNotExist:
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
                offer_letter_attachment = form.cleaned_data['offer_letter_attachment']
                if request.FILES.get('offer_letter_attachment', ""):
                    form.offer_letter_attachment = request.FILES['offer_letter_attachment']

                PreviousEmployment(employee=employee,
                company_name=company_name,
                company_address=company_address,
                job_type=job_type,
                employed_from=employed_from,
                employed_upto=employed_upto,
                last_ctc=last_ctc,
                reason_for_exit=reason_for_exit,
                ps_attachment=ps_attachment,
                rl_attachment=rl_attachment,
                offer_letter_attachment=offer_letter_attachment).save()
                context['form'] = form
                return render(request, 'form_templates/previous.html',context)

        else:
            print form.is_valid()
            # import ipdb; ipdb.set_trace()
            company_name_errors = form['company_name'].errors
            company_address_errors = form['company_address'].errors
            job_type_errors = form['job_type'].errors
            employed_from_errors = form['employed_from'].errors
            employed_upto_errors = form['employed_upto'].errors
            last_ctc_errors = form['last_ctc'].errors
            reason_for_exit_errors = form['reason_for_exit'].errors
            
            return render(request, 'form_templates/previous.html', {'form':form, 'company_name_errors':company_name_errors,
            'company_address_errors':company_address_errors,'job_type_errors':job_type_errors,'employed_from_errors':employed_from_errors,
            'employed_upto_errors':employed_upto_errors,'last_ctc_errors':last_ctc_errors,'reason_for_exit_errors':reason_for_exit_errors})

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
    offer_letter_attachment = form.cleaned_data['offer_letter_attachment']
    if request.FILES.get('offer_letter_attachment', ""):
        form.offer_letter_attachment = request.FILES['offer_letter_attachment']

    PreviousEmployment(employee=employee,
    company_name=company_name,
    company_address=company_address,
    job_type=job_type,
    employed_from=employed_from,
    employed_upto=employed_upto,
    last_ctc=last_ctc,
    reason_for_exit=reason_for_exit,
    ps_attachment=ps_attachment,
    rl_attachment=rl_attachment,
    offer_letter_attachment=offer_letter_attachment).save()
    context['form'] = form
    return render(request, 'form_templates/previous.html',context)

@csrf_exempt
@login_required
def confirm(request):
    
    if request.user.is_authenticated:

        if request.method == 'GET':
            context = {"form":""}
            form = ProofForm()
            context["form"] = form
            # import ipdb; ipdb.set_trace()
            user = request.user
            try:
                employee=UserDetails.objects.get(employee=request.user)
                try:
                    proof=Proof.objects.get(employee=request.user)   
                except Proof.DoesNotExist:
                    messages.error(request, 'Please fill all your proof details before confirming')
                    
                    return render(request,'form_templates/confirm.html', context)
            except UserDetails.DoesNotExist:
                messages.error(request, 'Please fill all your User details before confirming')
                context["form"] = form
                return render(request,'form_templates/confirm.html', context)

            name_pan = employee.name_pan
            nationality = employee.nationality
            blood_group = employee.blood_group
            land_phone = employee.land_phone
            mobile_phone = employee.mobile_phone
            gender = employee.gender

            context = {
            'employee':employee,
            'name_pan':name_pan,
            'nationality':nationality,
            'blood_group':blood_group,
            'land_phone':land_phone,
            'mobile_phone':mobile_phone,
            'gender':gender,
            }

            context.update(csrf(request))

            return render(request, 'form_templates/confirm.html',context)
    else:
        return HttpResponseRedirect('/login')

def download_form(request):
    return render(request, 'download_forms.html',{})

def candidate_overview(request):
    return render(request, 'candidate_overview.html',{})

def print_candidate_information(request):

    if request.method == 'GET':
        # import ipdb; ipdb.set_trace()
        context = {"form":"","education_form":"","previous_employment_form":"","proof_form":""}
        form = UserDetailsForm()
        education_form = EducationForm()
        previous_employment_form = PreviousEmploymentForm()
        proof_form = ProofForm()
        context["form","education_form","previous_employment_form","proof_form"] = form,education_form,previous_employment_form,proof_form
        
        try:
            employee = UserDetails.objects.get(employee=request.user)
            name_pan = employee.name_pan
            nationality = employee.nationality
            date_of_birth = employee.date_of_birth
            blood_group = employee.blood_group
            land_phone = employee.land_phone
            mobile_phone = employee.mobile_phone
            gender = employee.gender
        except UserDetails.DoesNotExist:
            messages.error(request, 'Please fill all your user details before printing')
            
            return HttpResponseRedirect('/user_details')

        try:
            
            address = Address.objects.get(employee=request.user, address_type ='PR')
            address_type = address.address_type
            address1 = address.address1
            address2 = address.address2
            city = address.city
            state = address.state
            zipcode = address.zipcode
            try:
                address_t = Address.objects.get(employee=request.user, address_type='TM')
                address_type = address_t.address_type
                address1 = address_t.address1
                address2 = address_t.address2
                city = address_t.city
                state = address_t.state
                zipcode = address_t.zipcode

            except Address.DoesNotExist:
                messages.error(request, 'Please fill all your address details before printing')
                
                return HttpResponseRedirect('/user_details')
        except Address.DoesNotExist:
            messages.error(request, 'Please fill all your address details before printing')
                
            return HttpResponseRedirect('/user_details')

        try:
            family = FamilyDetails.objects.get(employee=request.user)
            marital_status = family.marital_status
            wedding_date = family.wedding_date
            spouse_name = family.spouse_name
            no_of_children = family.no_of_children
            mother_name = family.mother_name
            mother_dob = family.mother_dob
            mother_profession = family.mother_profession
            father_name = family.father_name
            father_profession = family.father_profession
            father_dob = family.father_dob
            emergency_phone1 = family.emergency_phone1
            emergency_phone2 = family.emergency_phone2
            child1_name = family.child1_name
            child2_name = family.child2_name
        except FamilyDetails.DoesNotExist:
            messages.error(request, 'Please fill all your family details before printing')
            
            return HttpResponseRedirect('/user_details/family_details')

        try:
            # import ipdb; ipdb.set_trace()
            education = Education.objects.get(employee=request.user, qualification='SSC')
            education_type = education.education_type
            qualification = education.qualification
            specialization = education.specialization
            from_date= education.from_date
            to_date = education.to_date
            institute = education.institute
            board_university = education.board_university
            overall_marks = education.overall_marks
        except Education.DoesNotExist:
            messages.error(request, 'Please fill all your education details before printing')
            
            return HttpResponseRedirect('/user_details/education')

        try:
            previous = PreviousEmployment.objects.get(employee=request.user)
            company_name = previous.company_name
            company_address = previous.company_name
            job_type = previous.job_type
            employed_from = previous.employed_from
            employed_upto = previous.employed_upto
            last_ctc = previous.last_ctc
            reason_for_exit = previous.reason_for_exit
        except PreviousEmployment.DoesNotExist:
            messages.error(request, 'Please fill all your previous employment details before printing')
            
            return HttpResponseRedirect('/user_details/previous_employment')

        try:
            proof = Proof.objects.get(employee=request.user)
            pan = proof.pan
            aadhar_card = proof.aadhar_card
            dl = proof.dl
            passport = proof.passport
            voter_id = proof.voter_id
        except Proof.DoesNotExist:
            messages.error(request, 'Please fill all your proof details before printing')
            
            return HttpResponseRedirect('/user_details/proof')
        
        context = {'employee':employee,'address':address,
            'name_pan':name_pan,
            'date_of_birth':date_of_birth,
            'nationality':nationality,
            'blood_group':blood_group,
            'land_phone':land_phone,
            'mobile_phone':mobile_phone,
            'gender':gender,

            'address_type':address_type,
            'address1':address1,
            'address2':address2,
            'city':city,
            'state':state,
            'zipcode':zipcode,

            'education_type':education_type,
            'qualification':qualification,
            'specialization':specialization,
            'from_date':from_date,
            'to_date':to_date,
            'institute':institute,
            'board_university':board_university,
            'overall_marks':overall_marks,

            'marital_status':marital_status,
            'wedding_date':wedding_date,
            'spouse_name':spouse_name,
            'no_of_children':no_of_children,
            'mother_name':mother_name,
            'mother_dob':mother_dob,
            'mother_profession':mother_profession,
            'father_name':father_name,
            'father_profession':father_profession,
            'father_dob':father_dob,
            'emergency_phone1':emergency_phone1,
            'emergency_phone2':emergency_phone2,
            'child1_name':child1_name,
            'child2_name':child2_name,

            'company_name' : company_name,
            'company_address' : company_address,
            'job_type' : job_type,
            'employed_from' : employed_from,
            'employed_upto' : employed_upto,
            'last_ctc' : last_ctc,
            'reason_for_exit' : reason_for_exit,

            'pan' : pan,
            'aadhar_card' : aadhar_card,
            'dl' : dl,
            'passport' : passport,
            'voter_id' : voter_id
            }


    return render(request, 'print.html',context)