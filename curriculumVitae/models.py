from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User

# Create your models here.


class DynamiCV(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    description=models.CharField(blank=True, max_length=255)
    keywords=models.CharField(blank=True, max_length=255)
    videourl=models.CharField(blank=True,max_length=255)
    biolink=models.CharField(blank=True,max_length=255)
    educationstatus=models.CharField(blank=True,max_length=255)
    employmentstatus=models.CharField(blank=True,max_length=255)
    birthdate=models.DateField(blank=True)

    def __str__(self):
        return self.user.username


class Education(models.Model):
    edu=models.ForeignKey(DynamiCV, on_delete=models.CASCADE)
    school=models.CharField(max_length=150, blank=True)
    unit=models.CharField(max_length=150, blank=True)
    department=models.CharField(max_length=150, blank=True)
    level=models.CharField(max_length=150, blank=True)
    startdate=models.DateField(blank=True)
    enddate=models.DateField(blank=True)
    grade=models.CharField(max_length=70, blank=True)
    order=models.IntegerField(blank=True)

    def __str__(self):
        return self.school
    
class Experience(models.Model):
    exp=models.ForeignKey(DynamiCV, on_delete=models.CASCADE)
    position=models.CharField(max_length=150, blank=True)
    title=models.CharField(max_length=150, blank=True)
    workplace=models.CharField(max_length=150, blank=True)
    description=models.CharField(max_length=255, blank=True)
    startdate=models.DateField(blank=True)
    enddate=models.DateField(blank=True)
    order=models.IntegerField(blank=True)

    def __str__(self):
        return self.position
    
class Skill(models.Model):
    COLOR=(
        ('primary', 'primary'),
        ('warning', 'warning'),
        ('danger', 'danger'),
        ('dark', 'dark'),
        ('info', 'info'),
        ('success', 'success'),

    ) 

    skill=models.ForeignKey(DynamiCV, on_delete=models.CASCADE)
    color=models.CharField(max_length=10, choices=COLOR, default='primary')
    skillname=models.CharField(max_length=150, blank=True)
    skillgrade=order=models.IntegerField(blank=True)
    certificate=models.CharField(max_length=150, blank=True)
    certimage=models.ImageField(blank=True, upload_to='images/users/')
    certificateurl=models.CharField(max_length=150, blank=True)
    certificatcode=models.CharField(max_length=150, blank=True)
    certorg=models.CharField(max_length=150, blank=True)
    description=models.CharField(max_length=255, blank=True)
    startdate=models.DateField(blank=True)
    enddate=models.DateField(blank=True)
    order=models.IntegerField(blank=True)

    def __str__(self):
        return self.skillname


class MessageForm(models.Model):
    STATUS=(
        ('New', 'New'),
        ('Read', 'Read'),
    ) 
    name=models.CharField(blank=True, max_length=25)
    email=models.CharField(blank=True, max_length=50)
    subject=models.CharField(blank=True, max_length=50)
    message=models.TextField(blank=True, max_length=255)
    status=models.CharField(max_length=10, choices=STATUS, default='New')
    ip=models.CharField(blank=True, max_length=25)
    create_at=models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name
    

class Form(ModelForm):
    class Meta:
        model=MessageForm
        fields= ['name','email','subject', 'message']
        widgets= {
        }

class ListMail(models.Model):
    email=models.EmailField(blank=True)
    ip=models.CharField(blank=True, max_length=25)
    create_at=models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.email
    
class ListMailForm(ModelForm):
    class Meta:
        model=ListMail
        fields= ['email','ip',]
        widgets= {
        }


    