from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()
import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'groupieserver.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    # url(r'^login/$', views.login, name='login'),
    url(r'^test/$', views.test, name='test'),		# works


    url(r'^signup/$', views.signup, name='signup'),	# works
    url(r'^test_logged_in', views.test_logged_in),  # works
    url(r'^person/(?P<pk>\d+)/$', views.get_person_details), # works


    # url(r'^home/$', views.home),

    url(r'^leaderboard/global/$', views.global_leaderboard),
    url(r'^leaderboard/group/(?P<pk>\d+)/$', views.group_leaderboard),
    


    url(r'^groups/new/$', views.create_group), # works
    url(r'^groups/delete/(?P<pk>\d+)/$', views.delete_group), #works
    url(r'^groups/(?P<pk>\d+)/$', views.get_group_details), # works

    url(r'^groups/join/(?P<pk>\d+)/$', views.join_group), # works
    url(r'^groups/leave/(?P<pk>\d+)/$', views.leave_group), # works
    url(r'^groups/code/change/(?P<pk>\d+)/$', views.change_joining_code),

    url(r'^groups/assignadmin/(?P<group_pk>\d+)/(?P<person_pk>\d+)/$', views.assign_admin), # works
    url(r'^groups/removeadmin/(?P<group_pk>\d+)/(?P<person_pk>\d+)/$', views.remove_admin), # works


    url(r'^posts/new/(?P<group_pk>\d+)/$', views.create_new_post), # works
    url(r'^posts/(?P<pk>\d+)/$', views.get_post_details), # works
    url(r'^posts/delete/(?P<pk>\d+)/$', views.delete_post),  # works


    # assign a task specifically to a person
    url(r'^tasks/new/(?P<group_pk>\d+)/(?P<person_pk>\d+)/$', views.create_task_specific_to_person), # works
    url(r'^tasks/new/(?P<group_pk>\d+)/$', views.create_task), # works
    url(r'^tasks/(?P<pk>\d+)/$', views.get_task_details),  # works
    url(r'^tasks/delete/(?P<pk>\d+)/$', views.delete_task), # works

    url(r'^tasks/accept/(?P<pk>\d+)/$', views.accept_task), # works
    url(r'^tasks/reject/(?P<pk>\d+)/$', views.reject_task), # works
    url(r'^tasks/complete/(?P<pk>\d+)/(?P<person_pk>\d+)/$', views.complete_task), # works

)