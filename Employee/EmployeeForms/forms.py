from django import forms
from django.contrib.auth.models import User
import datetime
import calendar
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from bootstrap3_datetime.widgets import DateTimePicker
from models import Address, UserDetails, Education, PreviousEmployment, Proof,GENDER_CHOICES,BLOOD_GROUP_CHOICES,MARITAL_CHOICES,QUALIFICATION,ADDRESSTYPE_CHOICES
dateTimeOption = {"format": "YYYY-MM-DD", "pickTime": False}

class UserRegistrationForm(UserCreationForm):
	email = forms.EmailField(required=True)
	first_name = forms.CharField(required=True)
	last_name = forms.CharField(required=True)

	class Meta:
		model = User
		fields = ('username','first_name', 'last_name','email', 'password1', 'password2')

	def save(self, commit=True):
		user = super(UserRegistrationForm, self).save(commit=False)
		user.email = self.cleaned_data['email']

		if commit:
			user.save()
		return user

class UserDetailsForm(forms.ModelForm):

	employee = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'width-50 input-sm form-control',
		'required': 'True', 'data-error': 'Please enter your name'}))
	first_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'width-50 input-sm form-control',
		'required': 'True', 'data-error': 'Please enter your first name'}))
	last_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'width-50 input-sm form-control',
		'required': 'True', 'data-error': 'Please enter your last name'}))
	middle_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'width-50 input-sm form-control',
		'required': 'False', 'data-error': 'Please enter your middle name'}))
	nationality = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'width-50 input-sm form-control','required': 'True'}))
	marital_status = forms.ChoiceField(choices=MARITAL_CHOICES)
	wedding_date = forms.DateField(widget=DateTimePicker(options=dateTimeOption),)
	wedding_date.widget.attrs = {'class': 'input-sm form-control filter_class', 'required': 'false'}
	# date_of_birth = forms.DateField(widget=DateTimePicker(options=dateTimeOption),)
	# date_of_birth.widget.attrs = {'class': 'input-sm form-control filter_class'}
	blood_group = forms.ChoiceField(choices=BLOOD_GROUP_CHOICES)
	land_phone =forms.RegexField(regex=r'^\+?1?\d{9,15}$',
		error_message=("Phone number must be entered in the format: '+999999999'. "
		"Up to 15 digits allowed."),
		widget=forms.TextInput(attrs={'class': 'width-30 input-sm form-control',
		'required': 'true','type': 'tel', 'pattern':'^\+?1?\d{9,15}$'}))
	emergency_phone = forms.RegexField(regex=r'^\+?1?\d{9,15}$',
		error_message=("Phone number must be entered in the format: '+999999999'. "
		"Up to 15 digits allowed."),
		widget=forms.TextInput(attrs={'class': 'width-30 input-sm form-control',
		'required': 'true','type': 'tel', 'pattern':'^\+?1?\d{9,15}$'}))
	#address = models.ForeignKey(Address)
	mobile_phone = forms.RegexField(regex=r'^\+?1?\d{9,15}$',
		error_message=("Phone number must be entered in the format: '+999999999'. "
		"Up to 15 digits allowed."),
		widget=forms.TextInput(attrs={'class': 'width-30 input-sm form-control',
		'required': 'true','type': 'tel', 'pattern':'^\+?1?\d{9,15}$'}))
	personal_email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'width-50 input-sm', 'type':'email'}))
	gender = forms.ChoiceField(choices=GENDER_CHOICES)

	class Meta:
		model = UserDetails
		exclude = ['employee']
		fields = ['first_name','last_name','middle_name','nationality','marital_status','wedding_date',
		'blood_group','land_phone','emergency_phone','mobile_phone','gender']

class EducationForm(forms.ModelForm):

	employee = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'width-50 input-sm form-control',
		'required': 'True', 'data-error': 'Please enter your name'}))
	qualification = forms.ChoiceField(choices=QUALIFICATION)
	specialization = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'width-50 input-sm form-control',
		'required': 'True'}))
	from_date = forms.DateField(widget=DateTimePicker(),)
	to_date = forms.DateField(widget=DateTimePicker(),)
	institution = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'width-50 input-sm form-control',
		'required': 'True'}))
	overall_marks = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'width-50 input-sm form-control',
		'required': 'True'}))


	class Meta:
		model = Education
		fields = ['qualification', 'specialization', 'from_date', 'to_date', 'institution', 'overall_marks']
		exclude = ['employee']

class PreviousEmploymentForm(forms.ModelForm):

	company_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'width-50 input-sm form-control',
		'required': 'True'}))
	#company_address = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'width-50 input-sm form-control',
		#'required': 'True'}))
	employed_from = forms.DateField(widget=DateTimePicker())
	employed_to = forms.DateField(widget=DateTimePicker())
	last_ctc = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class': 'width-50 input-sm form-control',
		'required': 'True'}))
	reason_for_exit = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'width-50 input-sm form-control',
		'required': 'False'}))

	class Meta:
		model = PreviousEmployment
		fields = ['company_name',  'employed_from', 'employed_to', 'employed_to', 'last_ctc','reason_for_exit']
		exclude = ['employee']

class ProofForm(forms.ModelForm):

	pan = forms.CharField(max_length=10, widget=forms.TextInput(attrs={'class': 'width-50 input-sm form-control',
		'required': 'True'}))
	aadhar_card = forms.CharField(max_length=12, widget=forms.TextInput(attrs={'class': 'width-50 input-sm form-control',
		'required': 'True'}))
	dl = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class': 'width-50 input-sm form-control',
		'required': 'False'}))
	passport = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class': 'width-50 input-sm form-control',
		'required': 'False'}))
	voter_id = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class': 'width-50 input-sm form-control',
		'required': 'False'}))

	class Meta:
		model = Proof
		fields = ['pan', 'aadhar_card', 'dl', 'passport', 'voter_id']
		exclude = ['employee']
