from django.conf.urls import url

from . import views

urlpatterns = [
        url(r'^$', views.index, name='index'),
        url(r'^upload/(?P<student_id>[0-9]*)&?(?P<hw_id>[0-9]*)&?(?P<acc_id>[0-9]*)', views.upload, name='upload'),
        url(r'^download_hw/(?P<student_id>[0-9]*)&?(?P<hw_id>[0-9]*)', views.download_hw, name='download_hw'),
        url(r'^download_doc/(?P<doc_type>\w+)/(?P<doc_id>\d+)', views.download_doc, name='download_doc'),
        url(r'^signup/', views.signup, name='signup'),
        url(r'^signin/', views.signin, name='signin'),
        url(r'^signout/', views.signout, name='signout'),

]
