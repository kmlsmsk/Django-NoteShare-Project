from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin
from content.models import CImages, ContentComment, Menu, Content

# Register your models here.
class ContentImageInline(admin.TabularInline):
    model=CImages
    extra=3

class MenuContentInline(admin.TabularInline):
    model=Content
    extra=1
    classes = ('collapse', )
    

class ContentAdmin(admin.ModelAdmin):
    list_display=['title', 'type', 'image_tag', 'status', 'create_at']
    list_filter=['status', 'type']
    inlines=[ContentImageInline]
    readonly_fields = ('image_tag',) 
    prepopulated_fields={'slug': ('title',)}
    
    
    

class MenuAdmin(DraggableMPTTAdmin):
    mptt_indent_field="title"
    list_display=('tree_actions', 'indented_title', 'status')
    list_filter=['status']
    inlines=[MenuContentInline]
    
    
class ContentCommentAdmin(admin.ModelAdmin):
    list_display=['subject', 'comment', 'content', 'user', 'status']
    list_filter=['status']

admin.site.register(ContentComment, ContentCommentAdmin)
admin.site.register(Menu, MenuAdmin)
admin.site.register(Content, ContentAdmin)
admin.site.register(CImages)

