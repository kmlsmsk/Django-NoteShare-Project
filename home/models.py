from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe 
from django.forms import ModelForm


class Settings(models.Model):
    STATUS=(
        ('True', 'Evet'),
        ('False', 'Hayir'),
    )        
    title=models.CharField(max_length=200)
    keywords=models.CharField(max_length=255)
    description=models.CharField(max_length=255)
    company=models.CharField(max_length=100)
    address=models.CharField(blank=True,max_length=150)
    googleMap=models.CharField(blank=True, max_length=255)
    phone=models.CharField(blank=True, max_length=20)
    fax=models.CharField(blank=True,max_length=20)
    email=models.CharField(blank=True, max_length=60)
    smtpserver=models.CharField(blank=True,max_length=30)
    smtpemail=models.CharField(blank=True,max_length=30)
    smtppassword=models.CharField(blank=True,max_length=30)
    smtpport=models.CharField(blank=True,max_length=10)
    icon=models.ImageField(blank=True, upload_to='images/')
    facebook=models.CharField(blank=True,max_length=50)
    instagram=models.CharField(blank=True,max_length=50)
    twitter=models.CharField(blank=True,max_length=50)
    youtube=models.CharField(blank=True,max_length=70)
    linkedin=models.CharField(blank=True,max_length=90)

    aboutus=RichTextUploadingField(blank=True)
    contact=RichTextUploadingField(blank=True)
    references=RichTextUploadingField(blank=True)

    status=models.CharField(max_length=10, choices=STATUS)
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True) 
    
    def __str__(self):
        return self.title
    
class ContactFormMessage(models.Model):
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
    note=models.CharField(blank=True, max_length=100)
    create_at=models.DateTimeField(auto_now_add=True, null=True)
    update_at=models.DateTimeField(auto_now=True, null=True)
    

    def __str__(self):
        return self.name


class ContactForm(ModelForm):
    class Meta:
        model=ContactFormMessage
        fields= ['name','email','subject', 'message']
        widgets= {

        }

class UserProfile(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    phone=models.CharField(blank=True, max_length=20)
    address=models.CharField(blank=True, max_length=150)
    city=models.CharField(blank=True, max_length=25)
    country=models.CharField(blank=True,max_length=25)
    image=models.ImageField(blank=True, upload_to='images/users/')

    def __str__(self):
        return self.user.username
    
    def user_name(self):
        return self.user.first_name+ ' '+self.user.last_name+' - [ '+self.user.username+ ' ] '
    
    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/> '.format(self.image.url))
    image_tag.short_description='Image'
    

class UserProfileForm(ModelForm):
    class Meta:
        model=UserProfile
        fields=['phone', 'address', 'city', 'country', 'image']



class FAQ(models.Model):
    STATUS=(
        ('True', 'Evet'),
        ('False', 'Hayir'),
    )        
    question=models.CharField(max_length=200)
    number=models.IntegerField()
    answer=models.TextField()
    status=models.CharField(max_length=10, choices=STATUS)
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True) 
    
    def __str__(self):
        return self.question