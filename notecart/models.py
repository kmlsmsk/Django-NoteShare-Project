from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm
from notes.models import Notes

class NoteCart(models.Model):
    user=models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    note=models.ForeignKey(Notes, on_delete=models.SET_NULL, null=True)
    quantity=models.IntegerField()
    

class NoteCartForm(ModelForm):
    class Meta:
        model=NoteCart
        fields=[ ]
