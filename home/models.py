from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Slide(models.Model):
    name = models.CharField(max_length=200)
    document = models.FileField(null=True, blank=True)
    def __str__(self):
        return self.name

class Homework(models.Model):
    name = models.CharField(max_length=200)
    ddl = models.DateTimeField()
    point = models.IntegerField(default=None)
    document = models.FileField(null=True, blank=True)
    def __str__(self):
        return self.name

class Accomplish(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    homework = models.ForeignKey(Homework, on_delete=models.CASCADE, default=None)
    submit = models.BooleanField(default=False)
    score = models.IntegerField(default=0)
    class Meta:
        unique_together = (("homework", "user"),)
    def __str__(self):
        username = self.user.username
        homework = self.homework.name
        return self.user.username + ' ' + self.homework.name

# handle upload and download of student homework
class Upload(models.Model):
    document = models.FileField(upload_to = 'home/upload/')
    uploaded_at = models.DateTimeField(auto_now_add = True)
    std_filename = models.CharField(max_length=200, blank=True, null=True)
    def __str__(self):
        return self.std_filename

class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    student_id = models.CharField(max_length=10)
    def __str__(self):
        return self.user.username + ' ' + self.student_id
User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])

class Lecture(models.Model):
    title = models.CharField(max_length = 200)
    time = models.DateTimeField()
    def __str__(self):
        return self.title
