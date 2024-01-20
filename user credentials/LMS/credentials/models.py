from django.db import models
from django.contrib.auth.models import User
    
class UserSubscription(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    duration_weeks = models.PositiveIntegerField()
    def __str__(self):
        return self.user.username


class Tutor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=None) 
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    mobile_number = models.CharField(max_length=13)
    
    def __str__(self):
        return self.name
    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    selected_subscription = models.ForeignKey(UserSubscription, on_delete=models.SET_NULL, null=True, blank=True)
   
    def __str__(self):
        return self.user.username
