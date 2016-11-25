from django import forms
from django.contrib.auth.models import User
import datetime
import calendar
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from bootstrap3_datetime.widgets import DateTimePicker
from django.utils.safestring import mark_safe
from models import Address, UserDetails, Education, PreviousEmployment, Proof, GENDER_CHOICES,BLOOD_GROUP_CHOICES,MARITAL_CHOICES,QUALIFICATION,ADDRESSTYPE_CHOICES, JOB_TYPE
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

	employee = forms.CharField(required=False)
	first_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'width-50 input-sm form-control',
		'required': 'True', 'data-error': 'Please enter your first name'}))
	last_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'width-50 input-sm form-control',
		'required': 'True', 'data-error': 'Please enter your last name'}))
	middle_name = forms.CharField(max_length=50,  required=False, widget=forms.TextInput(attrs={'class': 'width-50 input-sm form-control','data-error': 'Please enter your middle name'}))
	nationality = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'width-50 input-sm form-control','required': 'True'}))
	marital_status = forms.ChoiceField(choices=MARITAL_CHOICES,  required=False)
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

		fields = ['first_name','last_name','middle_name','nationality','marital_status','wedding_date',
		'blood_group','land_phone','emergency_phone','mobile_phone','gender']
		exclude = ['employee']

class EducationForm(forms.ModelForm):

	employee = forms.CharField(required=False)
	qualification = forms.ChoiceField(choices=QUALIFICATION)
	specialization = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'width-50 input-sm form-control',
		'required': 'True'}))
	from_date = forms.DateField(widget=DateTimePicker(),)
	to_date = forms.DateField(widget=DateTimePicker(),)
	institute = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'width-50 input-sm form-control',
		'required': 'True'}))
	overall_marks = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'width-50 input-sm form-control',
		'required': 'True'}))
	marks_card_attachment = forms.FileField(label='Marks Card Attachment', required=False)


	class Meta:
		model = Education
		fields = ['qualification', 'specialization', 'from_date', 'to_date', 'institute', 'overall_marks', 'marks_card_attachment']
		exclude = ['employee']

class PreviousEmploymentForm(forms.ModelForm):

	company_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'width-50 input-sm form-control',
		'required': 'True'}))
	company_address = forms.CharField(max_length=500, widget=forms.TextInput(attrs={'class': 'width-500 input-sm form-control',
		'required': 'True'}))
	job_type = forms.ChoiceField(choices=JOB_TYPE)
	employed_from = forms.DateField(widget=DateTimePicker())
	employed_upto = forms.DateField(widget=DateTimePicker())
	last_ctc = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class': 'width-50 input-sm form-control',
		'required': 'True'}))
	reason_for_exit = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'width-50 input-sm form-control',
		'required': 'False'}))
	ps_attachment = forms.FileField(label='Pay slips Attachment', required=False)
	rl_attachment = forms.FileField(label='Relieving Letter Attachment', required=False)

	class Meta:
		model = PreviousEmployment
		fields = ['company_name', 'company_address', 'job_type',  'employed_from', 'employed_upto', 'last_ctc','reason_for_exit', 'ps_attachment', 'rl_attachment']
		exclude = ['employee']

class ProofForm(forms.ModelForm):

	pan = forms.CharField(max_length=10, required=False, widget=forms.TextInput(attrs={'class': 'width-50 input-sm form-control'}))
	pan_attachment = forms.FileField(label='PAN Attachment',required=False)
	# Add Bootstrap widgets
	#pan_attachment.widget.attrs = {'class':'filestyle', 'data-buttonBefore':'true', 'data-iconName':'glyphicon glyphicon-paperclip'}
	aadhar_card = forms.CharField(max_length=12, required=False, widget=forms.TextInput(attrs={'class': 'width-50 input-sm form-control'}))
	aadhar_attachment = forms.FileField(label='Aadhar Card Attachment', required=False)
    # Add Bootstrap widgets
	#aadhar_attachment.widget.attrs = {'class':'filestyle', 'data-buttonBefore':'true', 'data-iconName':'glyphicon glyphicon-paperclip'}
	dl = forms.CharField(max_length=20, required=False, widget=forms.TextInput(attrs={'class': 'width-50 input-sm form-control'}))
	dl_attachment = forms.FileField(label='DL Attachment', required=False, help_text=mark_safe("Allowed file types: jpg, csv, png, pdf, xls, xlsx, doc, docx, jpeg.<br>Maximum allowed file size: 1MB"))
    # Add Bootstrap widgets
	#dl_attachment.widget.attrs = {'class':'filestyle', 'data-buttonBefore':'true', 'data-iconName':'glyphicon glyphicon-paperclip'}
	passport = forms.CharField(max_length=20, required=False, widget=forms.TextInput(attrs={'class': 'width-50 input-sm form-control'}))
	passport_attachment = forms.FileField(label='Passport Attachment', required=False, help_text=mark_safe("Allowed file types: jpg, csv, png, pdf, xls, xlsx, doc, docx, jpeg.<br>Maximum allowed file size: 1MB"))
    # Add Bootstrap widgets
	#passport_attachment.widget.attrs = {'class':'filestyle', 'data-buttonBefore':'true', 'data-iconName':'glyphicon glyphicon-paperclip'}
	voter_id = forms.CharField(max_length=20, required=False, widget=forms.TextInput(attrs={'class': 'width-50 input-sm form-control'}))
	voter_attachment = forms.FileField(label='Voter Attachment', required=False, help_text=mark_safe("Allowed file types: jpg, csv, png, pdf, xls, xlsx, doc, docx, jpeg.<br>Maximum allowed file size: 1MB"))
    # Add Bootstrap widgets
	#voter_attachment.widget.attrs = {'class':'filestyle', 'data-buttonBefore':'true', 'data-iconName':'glyphicon glyphicon-paperclip'}

	class Meta:
		model = Proof
		fields = ['pan','pan_attachment', 'aadhar_card','aadhar_attachment', 'dl','dl_attachment', 'passport','passport_attachment', 'voter_id','voter_attachment']
		exclude = ['employee']

# class FileUploadForm(forms.ModelForm):
#
#
# 	attachment = forms.FileField(label='Attachment', required=False, help_text=mark_safe("Allowed file types: jpg, csv, png, pdf, xls, xlsx, doc, docx, jpeg.<br>Maximum allowed file size: 1MB"))
#     # Add Bootstrap widgets
# 	attachment.widget.attrs = {'class':'filestyle', 'data-buttonBefore':'true', 'data-iconName':'glyphicon glyphicon-paperclip'}
# 	title = forms.CharField(max_length=10, widget=forms.TextInput(attrs={'class': 'width-50 input-sm form-control',
# 		'required': 'True'}))
#
#
# 	class Meta:
# 		model = FileUpload
# 		fields = ['title','attachment']
# 		exclude = ['employee']
