from django.db import models
from django.contrib.auth.models import User



class Hackathon(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length = 100)
    description = models.TextField()
    background_image = models.ImageField(upload_to='images/')
    hackathon_image = models.ImageField(upload_to='images/')
    type_submission = models.CharField(max_length = 100)
    start_time = models.CharField(max_length = 100)
    end_time = models.CharField(max_length = 100)
    reward = models.CharField(max_length = 100)
    verify_status = models.BooleanField(default=False)


class Registration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hackathon = models.ForeignKey(Hackathon, on_delete=models.CASCADE)
    status = models.BooleanField(null=False, default=True)

class Submissions(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hackathon = models.ForeignKey(Hackathon, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    summary = models.TextField()
    image_submission = models.ImageField(null=True)
    text_submission = models.TextField(null=True)
    link_submission = models.URLField(null=True)

