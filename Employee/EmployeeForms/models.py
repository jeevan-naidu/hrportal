from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator
from django.core.exceptions import ObjectDoesNotExist
import datetime, os
# fs = FileSystemStorage(location='EmployeeForms/emp_photo')
# Create your models here.

GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
    )

BLOOD_GROUP_CHOICES = (
    ('00', 'A+'),
    ('01', 'A-'),
    ('02', 'B+'),
    ('03', 'B-'),
    ('04', 'O+'),
    ('05', 'O-'),
    ('06', 'AB+'),
    ('07', 'AB-'),
    )

MARITAL_CHOICES = (
    ('MA', 'Married'),
    ('WD', 'Windowed'),
    ('SE', 'Seperated'),
    ('DV', 'Divorced'),
    ('SG', 'Single'),
    )

QUALIFICATION = (
	('SSC', 'Senior Secondary'),
	('HSC', 'Higher Secondary'),
	('GRAD', 'Graduate'),
	('PG', 'Post Graduate'),
	)

ADDRESSTYPE_CHOICES = (
    ('PR', 'Permanent'),
    ('TM', 'Temporary'),
    )

class Address(models.Model):

	# employee = models.ForeignKey(User)
	address_id = models.CharField(max_length=4)
	address_type = models.CharField('Address Type',max_length=2,choices=ADDRESSTYPE_CHOICES,default='TM')
	address1 = models.CharField(verbose_name="Address 1",max_length=100,blank=False)
	address2 = models.CharField(verbose_name="Address 2",max_length=100,blank=False)
	city = models.CharField("City", max_length=30, blank=False)
	state = models.CharField("State", max_length=30, blank=False)
	zipcode = models.CharField("Zip Code", max_length=10, blank=False)
	is_active = models.BooleanField("Current address is permanent address")

	def __unicode__(self):
		return u'{0}'.format(
			self.address_id,

			)

# class UserAddress(models.Model):

# 	employee = models.ForeignKey(User)
# 	address = models.ForeignKey(Address)

class UserDetails(models.Model):

	employee = models.ForeignKey(User)
	# first_name = models.CharField("First Name", max_length=15, blank=True)
	middle_name = models.CharField("Middle Name", max_length=15, blank=True, null=True)
	# last_name = models.CharField("Last Name", max_length=15, blank=True)
	gender = models.CharField("Gender", max_length=2,choices=GENDER_CHOICES,blank=False)
	nationality = models.CharField("Nationality", max_length=30, blank=False)
	marital_status = models.CharField("Marital Status",max_length=10,choices=MARITAL_CHOICES,blank=True, null=True)
	wedding_date = models.DateField(verbose_name='Wedding Date',null=True,blank=True)
	blood_group = models.CharField("Blood Group",max_length=3,choices=BLOOD_GROUP_CHOICES,blank=True)
	mobile_phone = models.CharField("Mobile Phone",max_length=15,unique=True,blank=False)
	land_phone = models.CharField("Landline Number",max_length=15, blank=True)
	emergency_phone = models.CharField("Emergency Contact Number",max_length=15,unique=True,blank=False)
	personal_email = models.EmailField("Personal E-mail",max_length=250,blank=False,unique=True)
	address = models.ManyToManyField(Address, verbose_name='User Address')

	#current_address = models.ForeignKey(Address)


	def __unicode__(self):
		return u'{0}'.format(

			self.employee)

class PreviousEmployment(models.Model):

	employee = models.ForeignKey(User)
	company_name = models.CharField("Company Name", max_length=150)
	company_address = models.ForeignKey(Address)
	employed_from = models.DateField(verbose_name="Start Date", null=False)
	employed_upto = models.DateField(verbose_name="End Date", null=False)
	pf_number = models.CharField("PF Number",max_length=15,null=True,blank=True)
	last_ctc = models.DecimalField("Last CTC",max_digits=15,decimal_places=2)
	reason_for_exit = models.CharField(verbose_name="Reason for Exit",max_length=50)
	createdon = models.DateTimeField(verbose_name="created Date",auto_now_add=True)
	updatedon = models.DateTimeField(verbose_name="Updated Date",auto_now=True)

	def __unicode__(self):
		return self.company_name + ':' + \
		str(self.employed_from) + ' ~ ' + str(self.employed_upto)



class Education(models.Model):

	employee = models.ForeignKey(User)
	qualification = models.CharField('Qualification', choices = QUALIFICATION, max_length = 5)
	specialization = models.CharField(verbose_name='Specialization',max_length=30,blank=True,null=True)
	from_date = models.DateField("From Date", blank=False)
	to_date = models.DateField("To Date", blank=False)
	institute = models.CharField("Institution", max_length=50, blank=False)
	overall_marks = models.IntegerField("Total Score/GPA",validators=[MaxValueValidator(100)],blank=False)

	def __unicode__(self):
		return u'{0}'.format(
			self.qualification,
			self.employee)

class Proof(models.Model):

	employee = models.ForeignKey(User)
	pan = models.CharField("PAN Number",max_length=10,blank=False,unique=True)
	aadhar_card = models.CharField("Aadhar Card",max_length=12,blank=True,unique=True)
	dl = models.CharField("Driving License", max_length=10,blank=True,unique=True)
	passport = models.CharField("Passport", max_length=10,blank=True,unique=True)
	voter_id = models.CharField("Voter ID", max_length=10,blank=True,unique=True)

	def __unicode__(self):
		return u'{0}'.format(
			self.employee)
