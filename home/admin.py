from django.contrib import admin
from .models import Slide, Homework, Accomplish, UserProfile, Upload

# Register your models here.
admin.site.register(Slide)
admin.site.register(Homework)
admin.site.register(Accomplish)
admin.site.register(UserProfile)
admin.site.register(Upload)
