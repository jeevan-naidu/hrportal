from __future__ import unicode_literals

from django.db import models
from sorl.thumbnail import ImageField
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
    ('A+', 'A+'),
    ('A-', 'A-'),
    ('B+', 'B+'),
    ('B-', 'B-'),
    ('O+', 'O+'),
    ('O-', 'O-'),
    ('AB+', 'AB+'),
    ('AB-', 'AB-'),
    )

MARITAL_CHOICES = (
    ('MA', 'Married'),
    ('SG', 'Single'),
    ('SE', 'Seperated'),
    ('DV', 'Divorced'),
    ('WD', 'Widowed'),
    )

JOB_TYPE = (
    ('FT', 'Full Time'),
    ('PT', 'Part Time'),
    ('CN', 'Contract'),
    ('IN', 'Intern'),
    )

EDUCATION_TYPE = (
    ('FT', 'Full Time'),
    ('PT', 'Part Time'),
    ('DS', 'Distance Education'),
    )

QUALIFICATION = (
	('SSC', 'Senior Secondary'),
    ('HSC', 'Higher Secondary'),
    ('GRAD', 'Graduate'),
	('PG', 'Post Graduate'),
    ('PhD', 'Doctrate'),
    ('Other', 'Others'),
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
    
    filetype = filename.split(".")[-1].lower()
    filename = filename
    path = "uploads/" + str(instance.employee)
    os_path = os.path.join(path, filename)
    return os_path

class ConfirmationCode(models.Model):
 
    username = models.ForeignKey(User, default=True)
    confirmation_code = models.CharField(verbose_name="Confirmation Code",max_length=100,blank=False, null = False, unique=True)

    def __unicode__(self):
        return u'{0}'.format(
            self.confirmation_code)

class Address(models.Model):

    class Meta:
        verbose_name_plural = 'Addresses'

    employee = models.ForeignKey(User, default=True)
    address_type = models.CharField('Address Type',max_length=2,choices=ADDRESSTYPE_CHOICES,default='PR')
    address1 = models.CharField(verbose_name="Address 1",max_length=200,blank=False)
    address2 = models.CharField(verbose_name="Address 2",max_length=200,blank=False)
    city = models.CharField("City", max_length=30, blank=False)
    state = models.CharField("State", max_length=30, blank=False)
    country = models.CharField("Country", max_length=30, blank=False,default="India")
    zipcode = models.CharField("Zip Code", max_length=10, blank=False)

    def __unicode__(self):
        return u'{0}'.format(
            self.address_type)

class UserDetails(models.Model):
    employee = models.ForeignKey(User, blank=True, null=True)
    name_pan = models.CharField("Name(as per PAN)", max_length=30, blank=True, null=True)
    photo = models.ImageField(upload_to=content_file_name,blank=True, null=True, verbose_name="Photo")
    gender = models.CharField("Gender", max_length=2,choices=GENDER_CHOICES,blank=False)
    nationality = models.CharField("Nationality", max_length=30, blank=False)
    date_of_birth = models.DateField(verbose_name='Date of Birth',null=True,blank=True)
    blood_group = models.CharField("Blood Group",max_length=3,choices=BLOOD_GROUP_CHOICES,blank=True)
    mobile_phone = models.CharField("Mobile Phone",max_length=10,unique=True,blank=False,null=True)
    land_phone = models.CharField("Landline Number", max_length=10,blank=True,null=True)
    address = models.ManyToManyField(Address, verbose_name='User Address')
    confirmation_code = models.CharField("Confirmation Code",max_length=15,unique=True,blank=True,null=True)
    def __unicode__(self):
        return u'{0}'.format(
            self.employee)

    def save(self, *args, **kwargs):
        # delete old file when replacing by updating the file
        try:
            this = UserDetails.objects.get(id=self.id)
            if this.image != self.image:
                this.image.delete(save=False)
        except: pass # when new photo then we do nothing, normal case          
        super(UserDetails, self).save(*args, **kwargs)

class LanguageProficiency(models.Model):

    employee = models.ForeignKey(User, blank=True, null=True)
    language_known = models.CharField(verbose_name='Language Known',max_length=50, null = True, blank=True)
    speak = models.NullBooleanField(verbose_name='Speak', default = False)
    write = models.NullBooleanField(verbose_name='Write', default = False)
    read = models.NullBooleanField(verbose_name='Read', default =False)
    def __unicode__(self):
        return u'{0}'.format(
            self.employee)

    class Meta:
        verbose_name = 'Language Proficiency'
        unique_together = ('language_known', 'employee')

class FamilyDetails(models.Model):
    employee = models.ForeignKey(User, blank=True, null=True)
    marital_status = models.CharField("Marital Status",max_length=10,choices=MARITAL_CHOICES,blank=True, null=True)
    wedding_date = models.DateField(verbose_name='Wedding Date',null=True,blank=True)
    spouse_name = models.CharField(verbose_name='Spouse Name',max_length=50,null=True,blank=True)
    spouse_dob = models.DateField(verbose_name='Spouse Name',max_length=50,null=True,blank=True)
    spouse_profession = models.CharField(verbose_name='Spouse Name',max_length=50,null=True,blank=True)
    no_of_children = models.CharField(verbose_name='Number of Children', max_length=10, null=True, blank=True)
    mother_name = models.CharField(verbose_name='Mother Name',max_length=30, null=False, blank=False)
    mother_dob = models.DateField(verbose_name='Mother Date of Birth',null=True,blank=True)
    mother_profession = models.CharField(verbose_name='Mother Profession',max_length=50,null=True,blank=True)
    father_name = models.CharField(verbose_name='Father Name',max_length=30)
    father_dob = models.DateField(verbose_name='Father Date of Birth',null=True,blank=True)
    father_profession = models.CharField(verbose_name='Father Profession',max_length=50,null=True,blank=True)
    emergency_phone1 = models.CharField("Emergency Contact Number1",max_length=10,unique=True,blank=True,null=True)
    emergency_phone2 = models.CharField("Emergency Contact Number2",max_length=10,unique=True,blank=True,null=True)
    child1_name = models.CharField(verbose_name='Child1 Name',max_length=30)
    child2_name = models.CharField(verbose_name='Child2 Name',max_length=30)
    def __unicode__(self):
        return u'{0}'.format(
            self.employee)

class PreviousEmployment(models.Model):
    employee = models.ForeignKey(User, blank=True, null=True)
    company_name = models.CharField("Company Name", max_length=150)
    company_address = models.CharField("Company Address",max_length=500, null=True)
    employed_from = models.DateField(verbose_name="Start Date", null=False)
    employed_upto = models.DateField(verbose_name="End Date", null=False)
    last_ctc = models.FloatField("Last CTC")
    reason_for_exit = models.CharField(verbose_name="Reason for Exit",max_length=200)
    job_type = models.CharField('Job Type', choices = JOB_TYPE, max_length = 5, default="PT")
    ps_attachment = models.FileField(upload_to=content_file_name,blank=True, null=True, verbose_name="Pay Slip Attachment")
    rl_attachment = models.FileField(upload_to=content_file_name,blank=True, null=True, verbose_name="Relieving letter Attachment")
    offer_letter_attachment = models.FileField(upload_to=content_file_name,blank=True, null=True, verbose_name="Offer letter Attachment")
    createdon = models.DateTimeField(verbose_name="created Date",auto_now_add=True)
    updatedon = models.DateTimeField(verbose_name="Updated Date",auto_now=True)
    def __unicode__(self):
        return self.company_name + ':' + \
        str(self.employed_from) + ' ~ ' + str(self.employed_upto)


class Education(models.Model):
    employee = models.ForeignKey(User, blank=True, null=True)
    education_type = models.CharField('Education Type', choices= EDUCATION_TYPE, max_length=5, default='FT')
    qualification = models.CharField('Qualification', choices = QUALIFICATION, max_length = 5)
    specialization = models.CharField(verbose_name='Specialization',max_length=30,blank=True,null=True)
    from_date = models.DateField("From Date", blank=False)
    to_date = models.DateField("To Date", blank=False)
    institute = models.CharField("Institution", max_length=50, blank=False)
    board_university = models.CharField("Board/University", max_length=50,blank=True,null=True)
    overall_marks = models.FloatField("Total Score/GPA",validators=[MaxValueValidator(100)],blank=False)
    marks_card_attachment = models.FileField(upload_to=content_file_name,blank=True, null=True, verbose_name="Marks card Attachment")
    def __unicode__(self):
        return u'{0},{1},{2}'.format(
            self.qualification,
            self.specialization,
            self.employee)

class EducationUniversity(models.Model):
    
    board_university = models.CharField("Board/University", max_length=50,blank=True,null=True)
    def __unicode__(self):
        return u'{0}'.format(
            self.board_university)

class EducationSpecialization(models.Model):

    specialization = models.CharField(verbose_name='Specialization',max_length=30,blank=True,null=True)
    def __unicode__(self):
        return u'{0}'.format(
            self.specialization)

class EducationInstitute(models.Model):

    institute = models.CharField(verbose_name='Institute',max_length=30,blank=True,null=True)
    def __unicode__(self):
        return u'{0}'.format(
            self.institute)

class Proof(models.Model):
    employee = models.ForeignKey(User, blank=True, null=True)
    pan = models.CharField("PAN Number",max_length=10,blank=False)
    pan_attachment = models.FileField(upload_to=content_file_name,blank=True, null=True, verbose_name="Pan Attachment")
    aadhar_card = models.CharField("Aadhar Card",max_length=12,blank=True)
    aadhar_attachment = models.FileField(upload_to=content_file_name,blank=True, null=True, verbose_name="Aadhar Card Attachment")
    dl = models.CharField("Driving License", max_length=15,blank=True, null=True)
    dl_attachment = models.FileField(upload_to=content_file_name,blank=True, null=True, verbose_name="DL Attachment")
    passport = models.CharField("Passport", max_length=10,blank=True,null=True)
    passport_attachment = models.FileField(upload_to=content_file_name,blank=True, null=True, verbose_name="Passport Attachment")
    voter_id = models.CharField("Voter ID", max_length=10, blank=True, null=True)
    voter_attachment = models.FileField(upload_to=content_file_name,blank=True, null=True, verbose_name="Voter ID Attachment")
    def __unicode__(self):
        return u'{0}'.format(
        self.employee)