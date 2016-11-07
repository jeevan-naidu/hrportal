from django.conf.urls import url, include, patterns
from django.contrib.auth.decorators import login_required
from EmployeeForms import views

urlpatterns = [
                       url(r'^$', (views.EmployeeWelcome), name=u'employee'),
                       url(r'^/login/$', views.login),
                       url(r'^/auth$', views.auth_view),
                       url(r'^/logout$', views.logout),
                       url(r'^/loggedin$', views.loggedin),
                       url(r'^/invalid$', views.invalid_login),
                       #url(r'^/password_change$', views.password_change),
                       url(r'^/register$', views.register),
                       url(r'^/register_success$', views.register_success),
                       url(r'^/user_details$', views.user_details, name=u'user_details'),
                       url(r'^/user_details/update$', views.user_update_details, name=u'user_update_details'), 
                       url(r'^/user_details/education$', views.education),
                       url(r'^/user_details/proof$', views.proof),
                       url(r'^/user_details/previous_employment$', views.previous_employment),
                       ]
