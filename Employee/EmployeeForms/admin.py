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
	list_display = [ 'address_type']

admin.site.register(UserDetails, UserDetailsAdmin)
admin.site.register(Education, EducationAdmin)
admin.site.register(Proof, ProofAdmin)
admin.site.register(PreviousEmployment, PreviousEmploymentAdmin)
admin.site.register(Address, AddressAdmin)
