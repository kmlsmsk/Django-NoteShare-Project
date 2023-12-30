from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin
# Register your models here.
from notes.models import Category, Comment, Notes, Images

class CategoryAdmin(admin.ModelAdmin):
    list_display=['title', 'status', 'create_at']
    list_filter=['status']


class ImagesAdmin(admin.ModelAdmin):
    list_display=['title', 'note', 'image_tag']
    readonly_fields = ('image_tag',)  #Eklenen komut (image_tag)


class NoteImageInline(admin.TabularInline):
    model=Images
    extra=3

class NoteAdmin(admin.ModelAdmin):
    list_display=['title', 'category', 'share', 'status','image_tag']
    list_filter=['status', 'category']
    inlines=[NoteImageInline]
    readonly_fields = ('image_tag',)  

    prepopulated_fields={'slug': ('title', )}

class CategoryAdmin2(DraggableMPTTAdmin):
    mptt_indent_field = "title"
    list_display = ('tree_actions', 'indented_title',
                    'related_products_count', 'related_products_cumulative_count')
    list_display_links = ('indented_title',)
    prepopulated_fields={'slug': ('title', )}

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Add cumulative product count
        qs = Category.objects.add_related_count(
                qs,
                Notes,
                'category',
                'products_cumulative_count',
                cumulative=True)

        # Add non cumulative product count
        qs = Category.objects.add_related_count(qs,
                 Notes,
                 'category',
                 'products_count',
                 cumulative=False)
        return qs

    def related_products_count(self, instance):
        return instance.products_count
    related_products_count.short_description = 'Related products (for this specific category)'

    def related_products_cumulative_count(self, instance):
        return instance.products_cumulative_count
    related_products_cumulative_count.short_description = 'Related products (in tree)'

class CommentAdmin(admin.ModelAdmin):
    list_display=['subject', 'comment', 'note', 'user', 'status']
    list_filter=['status']


admin.site.register(Comment, CommentAdmin)
admin.site.register(Images, ImagesAdmin)
admin.site.register(Category, CategoryAdmin2)
admin.site.register(Notes, NoteAdmin)
