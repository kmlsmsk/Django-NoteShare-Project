from django.contrib import admin
from notecart.models import NoteCart

class NoteCartAdmin(admin.ModelAdmin):
    list_display=['user', 'note', 'quantity']
    list_filter=['user']


admin.site.register(NoteCart, NoteCartAdmin)
