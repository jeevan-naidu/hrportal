from django import forms
from django.contrib.auth.models import User
import datetime
import calendar
from django.contrib.auth.forms import UserCreationForm
from bootstrap3_datetime.widgets import DateTimePicker
from django.utils.safestring import mark_safe
from models import Address, UserDetails, Education, PreviousEmployment, Proof, GENDER_CHOICES,BLOOD_GROUP_CHOICES,MARITAL_CHOICES,QUALIFICATION,ADDRESSTYPE_CHOICES, JOB_TYPE
dateTimeOption = {"format": "YYYY-MM-DD", "pickTime": False}

class UserRegistrationForm(UserCreationForm):
	username = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'width-100 input-sm form-control','required': 'True'}))
	first_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'width-100 input-sm form-control','required': 'True'}))
	last_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'width-100 input-sm form-control','required': 'True'}))
	email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'class': 'width-100 input-sm form-control','required': 'True','data-error': 'User with this email id exists'}))
	password1 = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'class': 'width-100 input-sm form-control','required': 'True'}))
	password2 = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'class': 'width-100 input-sm form-control','required': 'True'}))

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
	first_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'width-50 input-sm form-control',
		'required': 'True', 'data-error': 'Please enter your first name'}))
	last_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'width-50 input-sm form-control',
		'required': 'True', 'data-error': 'Please enter your last name'}))
	middle_name = forms.CharField(max_length=50,  required=False, widget=forms.TextInput(attrs={'class': 'width-50 input-sm form-control','data-error': 'Please enter your middle name'}))
	nationality = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'width-50 input-sm form-control','required': 'True'}))
	marital_status = forms.ChoiceField(choices=MARITAL_CHOICES,  required=False, widget=forms.Select(attrs={'class': 'width-50 input-sm form-control','required': 'False'}))
	wedding_date = forms.DateField(label="Wedding Date", required=False, widget=DateTimePicker(options=dateTimeOption),)
	wedding_date.widget.attrs = {'class': 'form-control filter_class'}
	date_of_birth = forms.DateField(label="Date of Birth",widget=DateTimePicker(options=dateTimeOption),)
	date_of_birth.widget.attrs = {'class': 'form-control filter_class', 'required':'true'}
	blood_group = forms.ChoiceField(choices=BLOOD_GROUP_CHOICES, widget=forms.Select(attrs={'class': 'width-50 input-sm form-control','required': 'False'}))
	land_phone =forms.CharField(max_length=10,required=False, widget=forms.TextInput(attrs={'class': 'width-30 input-sm form-control','type': 'tel'}))
	emergency_phone1 = forms.CharField(max_length=10, widget=forms.TextInput(attrs={'class': 'width-30 input-sm form-control','required': 'true','type': 'tel'}))
	emergency_phone2 = forms.CharField(max_length=10,widget=forms.TextInput(attrs={'class': 'width-30 input-sm form-control','required': 'true','type': 'tel'}))
	mobile_phone = forms.CharField(max_length=10,widget=forms.TextInput(attrs={'class': 'width-30 input-sm form-control','required': 'true','type': 'tel'}))
	personal_email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'width-50 input-sm', 'type':'email'}))
	gender = forms.ChoiceField(choices=GENDER_CHOICES, widget=forms.Select(attrs={'class': 'input-sm form-control','required': 'False'}))
	address_type = forms.ChoiceField(choices=ADDRESSTYPE_CHOICES, widget=forms.Select(attrs={'class': 'width-30 input-sm form-control','required': 'True'}))
	address1 = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'width-50 input-sm form-control','required': 'True'}))
	address2 = forms.CharField(max_length=200, required=False, widget=forms.TextInput(attrs={'class': 'width-50 input-sm form-control'}))
	city = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'width-30 input-sm form-control','required': 'True'}))
	state = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'width-30 input-sm form-control','required': 'True'}))
	zipcode = forms.CharField(max_length=10, widget=forms.TextInput(attrs={'class': 'width-30 input-sm form-control','required': 'True'}))
		
	class Meta:
		model = UserDetails

		fields = ['first_name','last_name','middle_name','nationality','marital_status','wedding_date','date_of_birth',
		'blood_group','land_phone','emergency_phone1','emergency_phone2','mobile_phone','gender']
		exclude = ['employee']

	class Meta:
		model = Address
		fields = ['address_type', 'address1', 'address2', 'city', 'state', 'zipcode' ]

class EducationForm(forms.ModelForm):

	employee = forms.CharField(required=False)
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

	class Meta:
		model = Education
		fields = ['qualification', 'specialization', 'from_date', 'to_date', 'institute', 'board_university', 'overall_marks', 'marks_card_attachment']
		exclude = ['employee']

	def clean(self):
		cleaned_data = self.cleaned_data
		to_date = cleaned_data.get('to_date')
		from_date = cleaned_data.get('from-date')
		if to_date and from_date:
			if to_date < from_date:
				self.add_error('to_date', 'Event end date should not occur before start date.')
            # You can use ValidationError as well
            # self.add_error('end_date', form.ValidationError('Event end date should not occur before start date.'))
    		return cleaned_data

class PreviousEmploymentForm(forms.ModelForm):

	company_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'input-sm form-control','required': 'True'}))
	company_address = forms.CharField(max_length=500, widget=forms.TextInput(attrs={'class': 'input-sm form-control','required': 'True'}))
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

	class Meta:
		model = PreviousEmployment
		fields = ['company_name', 'company_address', 'job_type',  'employed_from', 'employed_upto', 'last_ctc','reason_for_exit', 'ps_attachment', 'rl_attachment']
		exclude = ['employee']

	def clean(self):
		cleaned_data = self.cleaned_data
		employed_upto = cleaned_data.get('employed_upto')
		employed_from = cleaned_data.get('employed_from')
		if employed_upto and employed_from:
			if employed_upto < employed_from:
				self.add_error('employed_upto', 'Event end date should not occur before start date.')
            # You can use ValidationError as well
            # self.add_error('end_date', form.ValidationError('Event end date should not occur before start date.'))
    		return cleaned_data

class ProofForm(forms.ModelForm):

	pan = forms.CharField(max_length=10, required=False, widget=forms.TextInput(attrs={'class': 'width-30 input-sm form-control'}))
	pan_attachment = forms.FileField(label='Pan Attachment', required=False, help_text=mark_safe("Allowed file types: jpg, csv, png, pdf, xls, xlsx, doc, docx, jpeg.<br>Maximum allowed file size: 1MB"))
    # Add Bootstrap widgets
	pan_attachment.widget.attrs = {'class':'bare', 'data-buttonBefore':'true', 'data-iconName':'glyphicon glyphicon-paperclip'}
	aadhar_card = forms.CharField(max_length=12, required=False, widget=forms.TextInput(attrs={'class': 'width-30 input-sm form-control'}))
	aadhar_attachment = forms.FileField(label='Aadhar Card Attachment', required=False, help_text=mark_safe("Allowed file types: jpg, csv, png, pdf, xls, xlsx, doc, docx, jpeg.<br>Maximum allowed file size: 1MB"))
    # Add Bootstrap widgets
	aadhar_attachment.widget.attrs = {'class':'bare', 'data-buttonBefore':'true', 'data-iconName':'glyphicon glyphicon-paperclip'}
	dl = forms.CharField(max_length=15, required=False, widget=forms.TextInput(attrs={'class': 'width-30 input-sm form-control'}))
	dl_attachment = forms.FileField(label='DL Attachment', required=False, help_text=mark_safe("Allowed file types: jpg, csv, png, pdf, xls, xlsx, doc, docx, jpeg.<br>Maximum allowed file size: 1MB"))
    # Add Bootstrap widgets
	dl_attachment.widget.attrs = {'class':'bare', 'data-buttonBefore':'true', 'data-iconName':'glyphicon glyphicon-paperclip'}
	passport = forms.CharField(max_length=20, required=False, widget=forms.TextInput(attrs={'class': 'width-30 input-sm form-control'}))
	passport_attachment = forms.FileField(label='Passport Attachment', required=False, help_text=mark_safe("Allowed file types: jpg, csv, png, pdf, xls, xlsx, doc, docx, jpeg.<br>Maximum allowed file size: 1MB"))
    # Add Bootstrap widgets
	passport_attachment.widget.attrs = {'class':'bare', 'data-buttonBefore':'true', 'data-iconName':'glyphicon glyphicon-paperclip'}
	voter_id = forms.CharField(max_length=10, required=False, widget=forms.TextInput(attrs={'class': 'width-30 input-sm form-control'}))
	voter_attachment = forms.FileField(label='Voter ID Attachment', required=False, help_text=mark_safe("Allowed file types: jpg, csv, png, pdf, xls, xlsx, doc, docx, jpeg.<br>Maximum allowed file size: 1MB"))
    # Add Bootstrap widgets
	voter_attachment.widget.attrs = {'class':'bare', 'data-buttonBefore':'true', 'data-iconName':'glyphicon glyphicon-paperclip'}

	class Meta:
		model = Proof
		fields = ['pan','pan_attachment', 'aadhar_card','aadhar_attachment', 'dl','dl_attachment', 'passport','passport_attachment', 'voter_id','voter_attachment']
		exclude = ['employee']
