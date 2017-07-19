from django.contrib import admin
from django.contrib.auth.models import User
from .models import Slide, Homework, Accomplish, UserProfile, Upload, Lecture

def create_accomplish(modeladmin, request, queryset):
    for hw in queryset:
        for user in User.objects.all()[1:]:
            Accomplish.objects.create(user=user, homework=hw)
create_accomplish.short_description = "Create accomplish for this homework"

class HomeworkAdmin(admin.ModelAdmin):
    actions = [create_accomplish]

class AccomplishAdmin(admin.ModelAdmin):
    list_display = ['user', 'homework', 'submit', 'score']

admin.site.register(Slide)
admin.site.register(Homework, HomeworkAdmin)
admin.site.register(Accomplish, AccomplishAdmin)
admin.site.register(UserProfile)
admin.site.register(Upload)
admin.site.register(Lecture)
