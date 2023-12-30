from django.db import models
from django.forms import FileInput, ModelForm, Select, TextInput
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel
from django.urls import reverse
from ckeditor.widgets import CKEditorWidget
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.text import slugify

class Menu(MPTTModel):
    STATUS=(
        ('True', 'Evet'),
        ('False', 'Hayır'),
    )

    parent=TreeForeignKey('self', blank=True, null=True, related_name='children', on_delete=models.CASCADE)
    #content=models.OneToOneRel(Content, blank=True, on_delete=models.CASCADE)
    title=models.CharField(max_length=100, unique=True)
    status=models.CharField(max_length=10, choices=STATUS)
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)

    class MPTTMeta:
        order_insertion_by=['title']

    def __str__(self):
        full_path=[self.title]
        k=self.parent
        while k is not None:
            full_path.append(k.title)
            k=k.parent
        return ' / '.join(full_path[::-1])
    
    
class Content(models.Model):
    TYPE=(
        ('menu', 'menu'),
        ('haber', 'haber'),
        ('duyuru', 'duyuru'),
        ('etkinlik', 'etkinlik'),
    )

    STATUS=(
        ('True', 'Evet'),
        ('False', 'Hayır'),
    )
    user=models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    menu=models.OneToOneField(Menu, null=True, blank=True, on_delete=models.CASCADE)
    type=models.CharField(max_length=15,choices=TYPE)
    title=models.CharField(max_length=160)
    keywords=models.CharField(blank=True,max_length=255)
    description=models.CharField(blank=True, max_length=255)
    image=models.ImageField(blank=True, null=True, upload_to='images/')
    detail=RichTextUploadingField()
    slug=models.SlugField(null=False, unique=True)
    status=models.CharField(max_length=15, choices=STATUS)
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    def image_tag(self):
        return mark_safe('<img src="{}" height="40"/>'.format(self.image.url))
    image_tag.short_description="Image"

    def get_absolute_url(self):
        return reverse("content_detail", kwargs={"slug": self.slug})
    
    def save(self, *args, **kwargs):
        self.slug=slugify(self.title)
        super().save(args, kwargs)
    
class CImages(models.Model):
    content=models.ForeignKey(Content, on_delete=models.CASCADE)
    title=models.CharField(max_length=60, blank=True)
    image=models.ImageField(blank=True, upload_to='images/')

    def __str__(self):
        return self.title
    def image_tag(self):
        return mark_safe('<img src="{}" height="40"/>'.format(self.image.url))
    image_tag.short_description="Image"
    
class ContentImageForm(ModelForm):
    class Meta:
        model=CImages
        fields=['title', 'image']

class ContentForm(ModelForm):
    class Meta:
        model=Content
        fields=['type', 'title', 'keywords', 'description', 'image' , 'detail']
        
        widgets={
            'title': TextInput(attrs={'class': 'input', 'placeholder': 'title'}),
            
            'keywords': TextInput(attrs={'class': 'input', 'placeholder': 'keywords'}),
            'description': TextInput(attrs={'class': 'input', 'placeholder': 'description'}),
            'type': Select (attrs={'class': 'input', 'placeholder': 'type'}),
            'image': FileInput(attrs={'class': 'input', 'placeholder': 'image'}),
            'detail': CKEditorWidget(),            
        }

class AdminContentForm(ModelForm):
    class Meta:
        model=Content
        fields=['type', 'title', 'status','keywords', 'description', 'image' , 'detail']
        
        widgets={
            'title': TextInput(attrs={'class': 'input', 'placeholder': 'title'}),
            'status': Select (attrs={'class': 'input', 'placeholder': 'status'}),
            'keywords': TextInput(attrs={'class': 'input', 'placeholder': 'keywords'}),
            'description': TextInput(attrs={'class': 'input', 'placeholder': 'description'}),
            'type': Select (attrs={'class': 'input', 'placeholder': 'type'}),
            'image': FileInput(attrs={'class': 'input', 'placeholder': 'image'}),
            'detail': CKEditorWidget(),            
        }
    

class ContentComment(models.Model):
    STATUS=(
        ('New', 'Yeni'),
        ('True', 'Evet'),
        ('False', 'Hayır'),        
    )
    content=models.ForeignKey(Content, on_delete=models.CASCADE)
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    subject=models.CharField(max_length=60, blank=True)
    comment=models.TextField(max_length=250, blank=True)
    rate=models.IntegerField(blank=True)
    status=models.CharField(max_length=10, choices=STATUS, default='New')
    ip=models.CharField(blank=True, max_length=20)
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject
    
class ContentCommentForm(ModelForm):
    class Meta:
        model=ContentComment
        fields=['subject', 'comment', 'rate']
