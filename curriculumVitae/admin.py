from django.contrib import admin

from curriculumVitae.models import DynamiCV, Education, Experience, ListMail, MessageForm, Skill

# Register your models here.

class MessageFormAdmin(admin.ModelAdmin):
    list_display=['name','email', 'create_at', 'subject','message', 'status']
    list_filter=['status']

class ListMailAdmin(admin.ModelAdmin):
    list_display=['email', 'create_at']
    list_filter=['create_at']

class DynamiCVAdmin(admin.ModelAdmin):
    list_display=['user', 'description', 'videourl', 'educationstatus', 'employmentstatus', 'birthdate']
    list_filter=['birthdate']

class EducationAdmin(admin.ModelAdmin):
    list_display=['school', 'unit', 'department', 'level', 'startdate', 'enddate', 'grade', 'order']
    list_filter=['school']

class ExperienceAdmin(admin.ModelAdmin):
    list_display=['position', 'title', 'workplace', 'description','startdate', 'enddate', 'order']
    list_filter=['position', 'workplace']

class SkillAdmin(admin.ModelAdmin):
    list_display=['skillname', 'skillgrade']
    list_filter=['certorg']

admin.site.register(Skill, SkillAdmin)
admin.site.register(Experience, ExperienceAdmin)
admin.site.register(Education, EducationAdmin)
admin.site.register(DynamiCV, DynamiCVAdmin)
admin.site.register(ListMail, ListMailAdmin)
admin.site.register(MessageForm, MessageFormAdmin)