from django.contrib import admin
from home.models import FAQ, ContactFormMessage, Settings, UserProfile

class SettingsAdmin(admin.ModelAdmin):
    list_display=['title','keywords']

admin.site.register(Settings, SettingsAdmin)


class ContactFormMessageAdmin(admin.ModelAdmin):
    list_display=['name','email', 'subject','message', 'note', 'status']
    list_filter=['status']

class UserProfileAdmin(admin.ModelAdmin):
    list_display=['user_name', 'phone', 'address', 'city', 'country', 'image_tag']

class FAQAdmin(admin.ModelAdmin):
    list_display=['number', 'question','answer', 'status']
    list_filter=['status']

admin.site.register(ContactFormMessage, ContactFormMessageAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(FAQ, FAQAdmin)
