from django.urls import path
from curriculumVitae import views

urlpatterns = [
    path('', views.index, name='index'),
    path('cv/', views.cv, name='cv'),
    path('sendmessage', views.sendmessage, name='sendmessage'),
    path('contentcategory/', views.contentcategory, name='contentcategory'),
    path('news/', views.news, name='news'),
    path('contacts/', views.contacts, name='contacts'),
    path('search/', views.search, name='search'),
    path('search_auto/', views.search_auto, name='search_auto'),
    path('addlistmail/', views.addlistmail, name='addlistmail'),
    path('emaillist/', views.emaillist, name='emaillist'),
    path('deletemaillist/<int:id>', views.deletemaillist, name='deletemaillist'),
     path('skill/<int:id>', views.skill, name='skill'),

]
