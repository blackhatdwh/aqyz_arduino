from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Slide(models.Model):
    name = models.CharField(max_length=200)
    link = models.CharField(max_length=200)
    def __str__(self):
        return self.name

class Homework(models.Model):
    name = models.CharField(max_length=200)
    ddl = models.DateTimeField()
    point = models.IntegerField(default=None)
    link = models.CharField(max_length=200, blank=True, null=True)
    def __str__(self):
        return self.name

class Accomplish(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    homework = models.ForeignKey(Homework, on_delete=models.CASCADE, default=None)
    upload_link = models.CharField(max_length=200, default=None, blank=True, null=True)
    download_link = models.CharField(max_length=200, default=None, blank=True, null=True)
    submit = models.BooleanField(default=False)
    score = models.IntegerField(default=0)
    def __str__(self):
        username = self.user.username
        homework = self.homework.name
        return self.user.username + ' ' + self.homework.name

class Document(models.Model):
    document = models.FileField(upload_to = 'home/uploads/')
    uploaded_at = models.DateTimeField(auto_now_add = True)

class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    student_id = models.CharField(max_length = 10)
    def __str__(self):
        return self.user.username + ' ' + self.student_id
User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])
