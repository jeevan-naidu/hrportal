from django import forms
from django.contrib.auth.models import User
import datetime
import calendar
from django.contrib.auth.forms import UserCreationForm
from bootstrap3_datetime.widgets import DateTimePicker
from django.utils.safestring import mark_safe
from django.core.validators import MaxValueValidator
from models import Address, UserDetails, Education, PreviousEmployment, Proof, FamilyDetails, LanguageProficiency, GENDER_CHOICES,BLOOD_GROUP_CHOICES,MARITAL_CHOICES,QUALIFICATION,ADDRESSTYPE_CHOICES, JOB_TYPE, EDUCATION_TYPE
dateTimeOption = {"format": "MM/DD/YYYY", "pickTime": False}

class UserRegistrationForm(UserCreationForm):
	username = forms.CharField(required=True, widget=forms.TextInput())
	first_name = forms.CharField(required=True, widget=forms.TextInput())
	last_name = forms.CharField(required=True, widget=forms.TextInput())
	email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'required': 'True','data-error': 'User with this email id exists'}))
	password1 = forms.CharField(required=True, widget=forms.PasswordInput())
	password2 = forms.CharField(required=True, widget=forms.PasswordInput())

	class Meta:
		model = User
		fields = ('username','first_name', 'last_name','email', 'password1', 'password2')

	def clean_email(self):
        # Check that email is not duplicate
		username = self.cleaned_data["username"]
		email = self.cleaned_data["email"]
		users = User.objects.filter(email__iexact=email).exclude(username__iexact=username)
		if users:
			raise forms.ValidationError('A user with that email already exists.')
		return email

	def save(self, commit=True):
		user = super(UserRegistrationForm, self).save(commit=False)
		user.email = self.cleaned_data['email']

		if commit:
			user.save()
		return user



class UserDetailsForm(forms.ModelForm):

	employee = forms.CharField(required=False)
	name_pan = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'width-50 input-sm form-control',
		'required': 'True', 'data-error': 'Please enter your first name'}))
	photo = forms.FileField(label='Photo Attachment', required=False, help_text=mark_safe("Allowed file types: jpg, csv, png, pdf, xls, xlsx, doc, docx, jpeg.<br>Maximum allowed file size: 1MB"))
    # Add Bootstrap widgets
	photo.widget.attrs = {'class':'bare', 'data-buttonBefore':'true', 'data-iconName':'glyphicon glyphicon-paperclip'}
	nationality = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'width-50 input-sm form-control','required': 'True'}))
	date_of_birth = forms.DateField(label="Date of Birth",widget=DateTimePicker(options=dateTimeOption),)
	date_of_birth.widget.attrs = {'class': 'form-control filter_class', 'required':'true'}
	blood_group = forms.ChoiceField(choices=BLOOD_GROUP_CHOICES, widget=forms.Select(attrs={'class': 'width-50 input-sm form-control','required': 'False'}))
	land_phone = forms.RegexField(max_length=10,required=False, regex=r'^\+?1?\d{9,15}$',error_message=("Phone number must be entered in the format: '999999999'. ""It should be 10 digits."),
                                   widget=forms.TextInput(attrs={'class': 'width-30 input-sm form-control','type': 'tel', 'pattern':'^\+?1?\d{9,15}$'}))
	mobile_phone = forms.RegexField(max_length=10,regex=r'^\+?1?\d{9,15}$',error_message=("Phone number must be entered in the format: '999999999'. ""It should be 10 digits."),
                                   widget=forms.TextInput(attrs={'class': 'width-30 input-sm form-control','type': 'tel', 'pattern':'^\+?1?\d{9,15}$'}))
	gender = forms.ChoiceField(choices=GENDER_CHOICES, widget=forms.Select(attrs={'class': 'input-sm form-control','required': 'False'}))
	address_type = forms.ChoiceField(choices=ADDRESSTYPE_CHOICES, widget=forms.Select(attrs={'class': 'width-30 input-sm form-control','required': 'True'}))
	address1 = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'width-50 input-sm form-control','required': 'True'}))
	address2 = forms.CharField(max_length=200, required=False, widget=forms.TextInput(attrs={'class': 'width-50 input-sm form-control'}))
	city = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'width-30 input-sm form-control','required': 'True'}))
	state = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'width-30 input-sm form-control','required': 'True'}))
	zipcode = forms.RegexField(max_length=6,required=False, regex=r'^\+?1?\d{5,6}$',error_message=("Please enter zipcode with 6 digits"),
                                   widget=forms.TextInput(attrs={'class': 'width-30 input-sm form-control','type': 'tel', 'pattern':'^\+?1?\d{5,6}$'}))
	# language_known = forms.CharField(required=False,max_length=50, widget=forms.TextInput(attrs={'class': 'width-50 input-sm form-control'}))
	# speak = forms.CharField(required=False,max_length=50, widget=forms.TextInput(attrs={'class': 'width-50 input-sm form-control'}))
	# read = forms.CharField(required=True,max_length=50, widget=forms.TextInput(attrs={'class': 'width-50 input-sm form-control'}))
	# write = forms.CharField(required=True,max_length=50, widget=forms.TextInput(attrs={'class': 'width-50 input-sm form-control'}))	
	
	class Meta:
		model = UserDetails

		fields = ['name_pan','photo','nationality','date_of_birth',
		'blood_group','land_phone','mobile_phone','gender']
		exclude = ['employee']

	class Meta:
		model = Address
		fields = ['address_type', 'address1', 'address2', 'city', 'state', 'zipcode' ]

	# class Meta:
	# 	model = LanguageProficiency
	# 	fields = ['language_known','speak','read','write']


class FamilyDetailsForm(forms.ModelForm):

	employee = forms.CharField(required=False)
	marital_status = forms.ChoiceField(choices=MARITAL_CHOICES,  required=False, widget=forms.Select(attrs={'class': 'width-50 input-sm form-control','required': 'False'}))
	wedding_date = forms.DateField(label="Wedding Date", required=False, widget=DateTimePicker(options=dateTimeOption),)
	wedding_date.widget.attrs = {'class': 'form-control filter_class'}
	spouse_name = forms.CharField(required=False,max_length=50, widget=forms.TextInput(attrs={'class': 'width-50 input-sm form-control'}))
	no_of_children = forms.CharField(required=False,max_length=50, widget=forms.TextInput(attrs={'class': 'width-50 input-sm form-control'}))
	mother_name = forms.CharField(required=True,max_length=50, widget=forms.TextInput(attrs={'class': 'width-50 input-sm form-control'}))
	mother_dob = forms.DateField(label="Mother Date of birth", required=False, widget=DateTimePicker(options=dateTimeOption),)
	mother_dob.widget.attrs = {'class': 'form-control filter_class'}
	mother_profession = forms.CharField(required=False,max_length=50, widget=forms.TextInput(attrs={'class': 'width-50 input-sm form-control'}))
	father_name = forms.CharField(required=True,max_length=50, widget=forms.TextInput(attrs={'class': 'width-50 input-sm form-control'}))
	father_dob = forms.DateField(label="Father Date of birth", required=False, widget=DateTimePicker(options=dateTimeOption),)
	father_dob.widget.attrs = {'class': 'form-control filter_class'}
	father_profession = forms.CharField(required=False,max_length=50, widget=forms.TextInput(attrs={'class': 'width-50 input-sm form-control'}))
	emergency_phone1 = forms.RegexField(max_length=10,regex=r'^\+?1?\d{9,15}$',error_message=("Phone number must be entered in the format: '999999999'.""It should be 10 digits."),
                                   widget=forms.TextInput(attrs={'class': 'width-30 input-sm form-control','type': 'tel', 'pattern':'^\+?1?\d{9,15}$'}))
	emergency_phone2 = forms.RegexField(max_length=10,regex=r'^\+?1?\d{9,15}$',error_message=("Phone number must be entered in the format: '999999999'. ""It should be 10 digits."),
                                   widget=forms.TextInput(attrs={'class': 'width-30 input-sm form-control','type': 'tel', 'pattern':'^\+?1?\d{9,15}$'}))
	child1_name = forms.CharField(required=False,max_length=50, widget=forms.TextInput(attrs={'class': 'width-50 input-sm form-control'}))
	child2_name = forms.CharField(required=False,max_length=50, widget=forms.TextInput(attrs={'class': 'width-50 input-sm form-control'}))

	class Meta:
		model = FamilyDetails
		fields = ['marital_status','wedding_date','spouse_name','no_of_children','mother_name','mother_dob','mother_profession',
		'father_name','father_dob','father_profession','emergency_phone1','emergency_phone2','child1_name','child2_name']

class EducationForm(forms.ModelForm):

	employee = forms.CharField(required=False)
	education_type = forms.ChoiceField(choices=EDUCATION_TYPE, widget=forms.Select(attrs={'class': 'width-100 input-sm form-control','required': 'True'}))
	qualification = forms.ChoiceField(choices=QUALIFICATION, widget=forms.Select(attrs={'class': 'width-100 input-sm form-control','required': 'True'}))
	specialization = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'width-100 input-sm form-control','required': 'True'}))
	from_date = forms.DateField(label="From date",widget=DateTimePicker(options=dateTimeOption),)
	from_date.widget.attrs = {'class': 'form-control filter_class', 'required':'true'}
	to_date = forms.DateField(label="To date",widget=DateTimePicker(options=dateTimeOption),)
	to_date.widget.attrs = {'class': 'form-control filter_class', 'required':'true'}
	institute = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'width-100 input-sm form-control','required': 'True'}))
	board_university = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'width-100 input-sm form-control','required': 'True'}))
	overall_marks = forms.FloatField(required=True, widget=forms.NumberInput(attrs={'min': '0', 'max': '100','placeholder': 'Marks float','data-error': 'Please enter marks in float and it should be below 100'}))
	marks_card_attachment = forms.FileField(label='Marks Card Attachment', required=False, help_text=mark_safe("Allowed file types: jpg, csv, png, pdf, xls, xlsx, doc, docx, jpeg.<br>Maximum allowed file size: 1MB"))
    # Add Bootstrap widgets
	marks_card_attachment.widget.attrs = {'class':'bare', 'data-buttonBefore':'true', 'data-iconName':'glyphicon glyphicon-paperclip'}

	def clean(self):
		from_date = self.cleaned_data.get("from_date")
		to_date = self.cleaned_data.get("to_date")
		if to_date < from_date:
			msg = u"End date should be greater than start date."
			self._errors["to_date"] = self.error_class([msg])

	class Meta:
		model = Education
		fields = ['education_type','qualification', 'specialization', 'from_date', 'to_date', 'institute', 'board_university', 'overall_marks', 'marks_card_attachment']
		exclude = ['employee']

	

class PreviousEmploymentForm(forms.ModelForm):

	company_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'input-sm form-control','required': 'True'}))
	company_address = forms.CharField(required=False, max_length=500, widget=forms.TextInput(attrs={'class': 'input-sm form-control'}))
	job_type = forms.ChoiceField(choices=JOB_TYPE, widget=forms.Select(attrs={'class': 'input-sm form-control','required': 'False'}))
	employed_from = forms.DateField(label="From date",widget=DateTimePicker(options=dateTimeOption),)
	employed_from.widget.attrs = {'class': 'form-control filter_class', 'required':'true'}
	employed_upto = forms.DateField(label="From date",widget=DateTimePicker(options=dateTimeOption),)
	employed_upto.widget.attrs = {'class': 'form-control filter_class', 'required':'true'}
	last_ctc = forms.FloatField(required=False, widget=forms.NumberInput(attrs={'placeholder': 'CTC float','data-error': 'Please enter your CTC in float'}))
	reason_for_exit = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'input-sm form-control','required': 'False'}))
	ps_attachment = forms.FileField(label='Pay slips Attachment', required=False, help_text=mark_safe("Allowed file types: jpg, csv, png, pdf, xls, xlsx, doc, docx, jpeg.<br>Maximum allowed file size: 1MB"))
    # Add Bootstrap widgets
	ps_attachment.widget.attrs = {'class':'bare', 'data-buttonBefore':'true', 'data-iconName':'glyphicon glyphicon-paperclip'}
	rl_attachment = forms.FileField(label='Relieveing Letter Attachment', required=False, help_text=mark_safe("Allowed file types: jpg, csv, png, pdf, xls, xlsx, doc, docx, jpeg.<br>Maximum allowed file size: 1MB"))
    # Add Bootstrap widgets
	rl_attachment.widget.attrs = {'class':'bare', 'data-buttonBefore':'true', 'data-iconName':'glyphicon glyphicon-paperclip'}
	offer_letter_attachment = forms.FileField(label='Offer Letter Attachment', required=False, help_text=mark_safe("Allowed file types: jpg, csv, png, pdf, xls, xlsx, doc, docx, jpeg.<br>Maximum allowed file size: 1MB"))
    # Add Bootstrap widgets
	offer_letter_attachment.widget.attrs = {'class':'bare', 'data-buttonBefore':'true', 'data-iconName':'glyphicon glyphicon-paperclip'}

	class Meta:
		model = PreviousEmployment
		fields = ['company_name', 'company_address', 'job_type',  'employed_from', 'employed_upto', 'last_ctc','reason_for_exit', 'ps_attachment', 'rl_attachment', 'offer_letter_attachment']
		exclude = ['employee']

class ProofForm(forms.ModelForm):

	pan = forms.RegexField(max_length=10,regex=r'^[A-Za-z]{5}[0-9]{4}[A-Za-z]{1}$',error_messages={'invalid': 'PAN number must be entered in the format: ABCDE1234F. It should be 10 digits.'},
                    widget=forms.TextInput(attrs={'class': 'width-30 input-sm form-control','type': 'tel', 'pattern':'^[A-Za-z]{5}[0-9]{4}[A-Za-z]{1}$'}))
	pan_attachment = forms.FileField(required=True, label='Pan Attachment', help_text=mark_safe("Allowed file types: jpg, csv, png, pdf, xls, xlsx, doc, docx, jpeg.<br>Maximum allowed file size: 1MB"))
    # Add Bootstrap widgets
	pan_attachment.widget.attrs = {'class':'bare', 'data-buttonBefore':'true', 'data-iconName':'glyphicon glyphicon-paperclip'}
	aadhar_card = forms.RegexField(max_length=12, regex=r'^[0-9]{12}$',error_message=("Aadhar number must be entered in the format: '1212121212'. ""It should be 12 digits."),
                    widget=forms.TextInput(attrs={'class': 'width-30 input-sm form-control','type': 'tel', 'pattern':'^[0-9]{12}$'}))
	aadhar_attachment = forms.FileField(label='Aadhar Card Attachment', required=False, help_text=mark_safe("Allowed file types: jpg, csv, png, pdf, xls, xlsx, doc, docx, jpeg.<br>Maximum allowed file size: 1MB"))
    # Add Bootstrap widgets
	aadhar_attachment.widget.attrs = {'class':'bare', 'data-buttonBefore':'true', 'data-iconName':'glyphicon glyphicon-paperclip'}
	dl = forms.CharField(max_length=10, required=False, widget=forms.TextInput(attrs={'class': 'width-30 input-sm form-control'}))
	dl_attachment = forms.FileField(label='DL Attachment', required=False, help_text=mark_safe("Allowed file types: jpg, csv, png, pdf, xls, xlsx, doc, docx, jpeg.<br>Maximum allowed file size: 1MB"))
    # Add Bootstrap widgets
	dl_attachment.widget.attrs = {'class':'bare', 'data-buttonBefore':'true', 'data-iconName':'glyphicon glyphicon-paperclip'}
	passport = forms.RegexField(max_length=8, regex=r'^[A-Za-z]{1}[0-9]{7}$',required=False, error_message=("Aadhar number must be entered in the format: '1212121212'. ""It should be 12 digits."),
                    widget=forms.TextInput(attrs={'class': 'width-30 input-sm form-control','type': 'tel', 'pattern':'^[A-Za-z]{1}[0-9]{7}$'}))
	passport_attachment = forms.FileField(label='Passport Attachment', required=False, help_text=mark_safe("Allowed file types: jpg, csv, png, pdf, xls, xlsx, doc, docx, jpeg.<br>Maximum allowed file size: 1MB"))
    # Add Bootstrap widgets
	passport_attachment.widget.attrs = {'class':'bare', 'data-buttonBefore':'true', 'data-iconName':'glyphicon glyphicon-paperclip'}
	voter_id = forms.RegexField(max_length=10, regex=r'^[A-Za-z]{3}[0-9]{7}$',required=False, error_message=("Aadhar number must be entered in the format: '1212121212'. ""It should be 12 digits."),
                    widget=forms.TextInput(attrs={'class': 'width-30 input-sm form-control','type': 'tel', 'pattern':'^[A-Za-z]{3}[0-9]{7}$'}))
	voter_attachment = forms.FileField(label='Voter ID Attachment', required=False, help_text=mark_safe("Allowed file types: jpg, csv, png, pdf, xls, xlsx, doc, docx, jpeg.<br>Maximum allowed file size: 1MB"))
    # Add Bootstrap widgets
	voter_attachment.widget.attrs = {'class':'bare', 'data-buttonBefore':'true', 'data-iconName':'glyphicon glyphicon-paperclip'}

	class Meta:
		model = Proof
		fields = ['pan','pan_attachment', 'aadhar_card','aadhar_attachment', 'dl','dl_attachment', 'passport','passport_attachment', 'voter_id','voter_attachment']
		exclude = ['employee']
