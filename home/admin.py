from django.contrib import admin
from .models import Slide, Homework, Accomplish, UserProfile

# Register your models here.
admin.site.register(Slide)
admin.site.register(Homework)
admin.site.register(Accomplish)
admin.site.register(UserProfile)
