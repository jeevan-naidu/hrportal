from django.conf.urls import url, include, patterns
from django.contrib.auth.decorators import login_required
from EmployeeForms.views import login
from axes.decorators import watch_login
from EmployeeForms import views

urlpatterns = [
                       # url(r'^$', (views.EmployeeWelcome), name=u'employee'),
                       url(r'^$', (views.register), name=u'employee'),
                       url(r'^confirmation/(?P<confirmation_code>\w+)/(?P<username>\w+)$', views.confirmation),
                       url(r'^user$', watch_login(login)),
                       url(r'^auth$', views.auth_view),
                       url(r'^logout$', views.logout),
                       url(r'^loggedin$', views.loggedin),
                       url(r'^login$', views.login),
                       url(r'^invalid$', views.invalid_login),
                       url(r'^register$', views.register),
                       url(r'^register_success$', views.register_success),
                       url(r'^user_details$', views.user_details),
                       url(r'^user_details/education_delete$', views.education_delete),
                       url(r'^user_details/address_copy$', views.address_copy),
                       url(r'^user_details/address_tempo$', views.address_tempo),
                       url(r'^user_details/previous_delete$', views.previous_delete),
                       url(r'^user_details/family_details$', views.family_details),
                       url(r'^user_details/education$', views.education),
                       url(r'^user_details/proof$', views.proof),
                       url(r'^user_details/previous_employment$', views.previous_employment),
                       url(r'^user_details/confirm$', views.confirm),
                       url(r'^download_form$', views.download_form),
                       url(r'^candidate_overview$', views.candidate_overview),
                       url(r'^print_candidate_information$', views.print_candidate_information),
                       url(r'^checkbox_check$', views.checkbox_check),
                       
                       url(r'^user_details/finish$', views.finish),
                       url(r'^user_details/sorry$', views.sorry),
                       
                       ]
