from django.contrib import admin
from models import *
# Register your models here.

class UserDetailsAdmin(admin.ModelAdmin):
	list_display = [ 'employee',]
	search_fields = ['employee']

class EducationAdmin(admin.ModelAdmin):
	list_display = [ 'employee','qualification']
	search_fields = ['user']

class ProofAdmin(admin.ModelAdmin):
	list_display = [ 'employee','pan','aadhar_card']
	search_fields = ['user']

class PreviousEmploymentAdmin(admin.ModelAdmin):
	list_display = [ 'employee',]
	search_fields = ['user']

class AddressAdmin(admin.ModelAdmin):
	list_display = [ 'employee','address_type']

class ConfirmationCodeAdmin(admin.ModelAdmin):
	list_display = [ 'confirmation_code', 'username']

class LanguageProfAdmin(admin.ModelAdmin):
	list_display = [ 'language_known', 'employee']

class FamilyDetailsAdmin(admin.ModelAdmin):
	list_display = [ 'employee']

class EduSpecAdmin(admin.ModelAdmin):
	list_display = [ 'specialization']

class EduUniAdmin(admin.ModelAdmin):
	list_display = [ 'board_university']

class EduInsAdmin(admin.ModelAdmin):
	list_display = [ 'institute' ]

admin.site.register(UserDetails, UserDetailsAdmin)
admin.site.register(Education, EducationAdmin)
admin.site.register(Proof, ProofAdmin)
admin.site.register(PreviousEmployment, PreviousEmploymentAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(ConfirmationCode, ConfirmationCodeAdmin)
admin.site.register(LanguageProficiency, LanguageProfAdmin)
admin.site.register(EducationUniversity, EduUniAdmin)
admin.site.register(EducationSpecialization, EduSpecAdmin)
admin.site.register(EducationInstitute, EduInsAdmin)
admin.site.register(FamilyDetails, FamilyDetailsAdmin)