from django.conf.urls import url

from . import views

urlpatterns = [
        url(r'^$', views.index, name='index'),
        url(r'^upload/(?P<student_id>[0-9]*)&?(?P<hw_id>[0-9]*)&?(?P<acc_id>[0-9]*)', views.upload, name='upload'),
]
