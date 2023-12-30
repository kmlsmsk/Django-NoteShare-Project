from django.db import models
from django.forms import FileInput, ModelForm, Select, TextInput
from django.urls import reverse
from django.utils.safestring import mark_safe   #Eklenen kütüphane
from ckeditor_uploader.fields import RichTextUploadingField
from ckeditor.widgets import CKEditorWidget
from mptt.models import MPTTModel, TreeForeignKey
from django.contrib.auth.models import User
from django.utils.text import slugify

class Category(MPTTModel):
    STATUS=(
        ('True', 'True'),
        ('False', 'False'),
    )
    title = models.CharField(max_length=120)
    keywords=models.CharField(max_length=255)
    description =models.CharField(max_length=255)
    image=models.ImageField(blank=True, upload_to='images/')
    status=models.CharField(max_length=10, choices=STATUS)
    slug=models.SlugField(null=False, unique=True)
    parent=TreeForeignKey('self', blank=True, null=True, related_name='children', on_delete=models.CASCADE)
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)

    class MPTTMeta:
        order_insertion_by = ['title']
       
    def __str__(self):
        full_path=[self.title]
        k=self.parent
        while k is not None:
            full_path.append(k.title)
            k=k.parent
        return ' / '.join(full_path[::-1])
    
    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})
    


class Notes(models.Model):
    STATUS=(
        ('True', 'Evet'),
        ('False', 'Hayır'),
        ('New', 'Yeni'),        
    )
    DURUM=(
        ('False', 'Hayır'),
        ('True', 'Evet'),
                
    )
    category=models.ForeignKey(Category, on_delete=models.CASCADE) #Kategori tablosu ile ilişki
    title=models.CharField(max_length=30)
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    keywords=models.CharField(max_length=255)
    description=models.CharField(max_length=255)
    image=models.ImageField(blank=True, upload_to='images/')
    filePdf = models.FileField(upload_to='pdfs/')
    share=models.CharField(max_length=10, choices=DURUM)
    detail=RichTextUploadingField()
    slug=models.SlugField(null=False, unique=True)
    status=models.CharField(max_length=10, choices=STATUS)
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    def image_tag(self):     #Eklenen Fonksiyon
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
    image_tag.short_description = 'Image'

    def get_absolute_url(self):
        return reverse('notes_detail', kwargs={'slug': self.slug})
    
    def save(self, *args, **kwargs):
        self.slug=slugify(self.title)
        super().save(args, kwargs)
    
  
class Images(models.Model):
    note=models.ForeignKey(Notes, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, blank=True)
    image=models.ImageField(blank=True, upload_to='images/')
    
    def __str__(self):
        return self.title
    
    def image_tag(self):  #Eklenen Fonksiyon
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
    image_tag.short_description = 'Image'

class Comment(models.Model):
    STATUS=(
        ('New', 'Yeni'),
        ('True', 'Evet'),
        ('False', 'Hayır'),        
    )
    note=models.ForeignKey(Notes, on_delete=models.CASCADE)
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
    
class CommentForm(ModelForm):
    class Meta:
        model=Comment
        fields=['subject', 'comment', 'rate']


class NotesForm(ModelForm):
    class Meta:
        model=Notes
        fields=['category', 'title', 'keywords', 'description', 'share', 'image', 'filePdf', 'detail']
        
        widgets={
            'category': Select (attrs={'class': 'input', 'placeholder': 'category'}, ),
            'title': TextInput(attrs={'class': 'input', 'placeholder': 'title'}),
            'keywords': TextInput(attrs={'class': 'input', 'placeholder': 'keywords'}),
            'description': TextInput(attrs={'class': 'input', 'placeholder': 'description'}),
            'share': Select (attrs={'class': 'input', 'placeholder': 'share'},  ),
            'image': FileInput(attrs={'class': 'input', 'placeholder': 'image'}),
            'filePdf': FileInput(attrs={'class': 'input', 'placeholder': 'filePdf'}),
            'detail': CKEditorWidget(),
                                    
        }
    
class AdminNotesForm(ModelForm):
    class Meta:
        model=Notes
        fields=['category', 'title', 'keywords', 'description', 'status','share', 'image', 'filePdf', 'detail']
        
        widgets={
            'category': Select (attrs={'class': 'input', 'placeholder': 'category'}, ),
            'title': TextInput(attrs={'class': 'input', 'placeholder': 'title'}),
            'keywords': TextInput(attrs={'class': 'input', 'placeholder': 'keywords'}),
            'description': TextInput(attrs={'class': 'input', 'placeholder': 'description'}),
            'status': Select (attrs={'class': 'input', 'placeholder': 'status'},  ),
            'share': Select (attrs={'class': 'input', 'placeholder': 'share'},  ),
            'image': FileInput(attrs={'class': 'input', 'placeholder': 'image'}),
            'filePdf': FileInput(attrs={'class': 'input', 'placeholder': 'filePdf'}),
            'detail': CKEditorWidget(),
                                    
        }
    

class NotesImageForm(ModelForm):
    class Meta:
        model=Images
        fields=['title', 'image']