from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator
from django.core.exceptions import ObjectDoesNotExist
import datetime, os
from django.core.files.storage import FileSystemStorage

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

JOB_TYPE = (
    ('FT', 'Full Time'),
    ('PT', 'Part Time'),
    ('CN', 'Contract'),
    ('IN', 'Intern'),
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

def content_file_name(instance, filename):
    ''' This function generates a random string of length 16 which will be a combination of (4 digits + 4
    characters(lowercase) + 4 digits + 4 characters(uppercase)) seperated 4 characters by hyphen(-) '''

    import random
    import string

    # random_str length will be 16 which will be combination of (4 digits + 4 characters + 4 digits + 4 characters)
    random_str =  "".join([random.choice(string.uppercase) for i in range(0,4)]) + "".join([random.choice(string.digits) for i in range(0,4)]) + \
                    "".join([random.choice(string.lowercase) for i in range(0,4)]) + "".join([random.choice(string.digits) for i in range(0,4)])

    # return string seperated by hyphen eg:
    random_str =  random_str[:4] + "-" + random_str[4:8] + "-" + random_str[8:12] + "-" + random_str[12:]
    filetype = filename.split(".")[-1].lower()
    filename = random_str +"." +  filetype
    path = "uploads/" + str(instance.employee)
    os_path = os.path.join(path, filename)
    return os_path

class Address(models.Model):

    class Meta:
        verbose_name_plural = 'Addresses'

    employee = models.ForeignKey(User, default=True)
    address_type = models.CharField('Address Type',max_length=2,choices=ADDRESSTYPE_CHOICES,default='PR')
    address1 = models.CharField(verbose_name="Address 1",max_length=100,blank=False)
    address2 = models.CharField(verbose_name="Address 2",max_length=100,blank=False)
    city = models.CharField("City", max_length=30, blank=False)
    state = models.CharField("State", max_length=30, blank=False)
    zipcode = models.CharField("Zip Code", max_length=10, blank=False)

    def __unicode__(self):
        return u'{0}, {1}, {2}, {3}, {4}'.format(
            self.address1,
            self.address2,
            self.city,
            self.state,
            self.zipcode)

class UserDetails(models.Model):
    employee = models.ForeignKey(User, blank=True, null=True)
    middle_name = models.CharField("Middle Name", max_length=15, blank=True, null=True)
    gender = models.CharField("Gender", max_length=2,choices=GENDER_CHOICES,blank=False)
    nationality = models.CharField("Nationality", max_length=30, blank=False)
    marital_status = models.CharField("Marital Status",max_length=10,choices=MARITAL_CHOICES,blank=True, null=True)
    wedding_date = models.DateField(verbose_name='Wedding Date',null=True,blank=True)
    blood_group = models.CharField("Blood Group",max_length=3,choices=BLOOD_GROUP_CHOICES,blank=True)
    mobile_phone = models.CharField("Mobile Phone",max_length=15,unique=True,blank=False)
    date_of_birth = models.CharField("Data of Birth",max_length=10, null=True, blank=True)
    land_phone = models.CharField("Landline Number",max_length=15, blank=True)
    emergency_phone = models.CharField("Emergency Contact Number",max_length=15,unique=True,blank=True,null=True)
    personal_email = models.EmailField("Personal E-mail",max_length=250,blank=False,unique=True)
    address = models.ManyToManyField(Address, verbose_name='User Address')
    def __unicode__(self):
        return u'{0}'.format(
            self.employee)

class PreviousEmployment(models.Model):
    employee = models.ForeignKey(User, blank=True, null=True)
    company_name = models.CharField("Company Name", max_length=150)
    company_address = models.CharField("Company Address",max_length=500, null=True)
    employed_from = models.DateField(verbose_name="Start Date", null=False)
    employed_upto = models.DateField(verbose_name="End Date", null=False)
    last_ctc = models.DecimalField("Last CTC",max_digits=15,decimal_places=2)
    reason_for_exit = models.CharField(verbose_name="Reason for Exit",max_length=50)
    job_type = models.CharField('Job Type', choices = JOB_TYPE, max_length = 5, default="PT")
    ps_attachment = models.FileField(upload_to=content_file_name,blank=True, null=True, verbose_name="Pay Slip Attachment")
    rl_attachment = models.FileField(upload_to=content_file_name,blank=True, null=True, verbose_name="Relieving letter Attachment")
    createdon = models.DateTimeField(verbose_name="created Date",auto_now_add=True)
    updatedon = models.DateTimeField(verbose_name="Updated Date",auto_now=True)
    def __unicode__(self):
        return self.company_name + ':' + \
        str(self.employed_from) + ' ~ ' + str(self.employed_upto)



class Education(models.Model):
    employee = models.ForeignKey(User, blank=True, null=True)
    qualification = models.CharField('Qualification', choices = QUALIFICATION, max_length = 5)
    specialization = models.CharField(verbose_name='Specialization',max_length=30,blank=True,null=True)
    from_date = models.DateField("From Date", blank=False)
    to_date = models.DateField("To Date", blank=False)
    institute = models.CharField("Institution", max_length=50, blank=False)
    overall_marks = models.IntegerField("Total Score/GPA",validators=[MaxValueValidator(100)],blank=False)
    marks_card_attachment = models.FileField(upload_to=content_file_name,blank=True, null=True, verbose_name="Marks card Attachment")
    def __unicode__(self):
        return u'{0}'.format(
            self.qualification,
            self.employee)

class Proof(models.Model):
    employee = models.ForeignKey(User, blank=True, null=True)
    pan = models.CharField("PAN Number",max_length=10,blank=False)
    pan_attachment = models.FileField(upload_to=content_file_name,blank=True, null=True, verbose_name="Pan Attachment")
    aadhar_card = models.CharField("Aadhar Card",max_length=12,blank=True)
    aadhar_attachment = models.FileField(upload_to=content_file_name,blank=True, null=True, verbose_name="Aadhar Card Attachment")
    dl = models.CharField("Driving License", max_length=10,blank=True, null=True)
    dl_attachment = models.FileField(upload_to=content_file_name,blank=True, null=True, verbose_name="DL Attachment")
    passport = models.CharField("Passport", max_length=10,blank=True,null=True)
    passport_attachment = models.FileField(upload_to=content_file_name,blank=True, null=True, verbose_name="Passport Attachment")
    voter_id = models.CharField("Voter ID", max_length=10,blank=True, null=True, unique=True)
    voter_attachment = models.FileField(upload_to=content_file_name,blank=True, null=True, verbose_name="Voter ID Attachment")
    def __unicode__(self):
        return u'{0}'.format(
        self.employee)

# class FileUpload(models.Model):
#     employee = models.ForeignKey(User)
#     title = models.CharField("Title",max_length=50,blank=False,unique=True)
#     attachment = models.FileField(upload_to=content_file_name, blank=True, null=True, verbose_name="Attachment")
#     def __unicode__(self):
#         return u'{0}'.format(self.employee)
