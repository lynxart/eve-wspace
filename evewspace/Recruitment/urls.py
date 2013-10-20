#    Eve W-Space
#    Copyright (C) 2013  Andrew Austin and other contributors
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version. An additional term under section
#    7 of the GPL is included in the LICENSE file.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
from django.conf.urls.defaults import patterns, include, url

apppatterns = patterns('Recruitment.views',
        url(r'edit/$', 'edit_app_type'),
        url(r'settings/$', 'app_global_settings'),
        url(r'stage/new/$', 'add_app_stage'),
        url(r'stage/(?P<stage_id>\d+)/delete/$', 'delete_app_stage'),
        url(r'stage/(?P<stage_id>\d+)/edit/$', 'edit_app_stage'),
        url(r'stage/(?P<stage_id>\d+)/question/new/$', 'new_question'),
        url(r'stage/(?P<stage_id>\d+)/question/(?P<question_id>\d+)/$', 'edit_question'),
        url(r'stage/(?P<stage_id>\d+)/question/(?P<question_id>\d+)/delete/$', 'delete_question'),
        url(r'delete/$', 'delete_app_type'),
        )


urlpatterns = patterns('Recruitment.views',
        url(r'register/$', 'applicant_register'),
        url(r'application/(?P<app_type_id>\d+)/$', 'get_application'),
        url(r'application/(?P<app_type_id>\d+)/', include(apppatterns)),
        url(r'applications/$', 'view_applications'),
        url(r'appeditor/$', 'edit_applications'),
        url(r'floweditor/$', 'edit_workflows'),
        url(r'settings/$', 'recruitment_settings'),
)
