from django.urls import path
from content import views

urlpatterns = [
    path('', views.index, name='index'),
    path('comments/', views.comments, name='comments'),
    path('contentComment/<int:id>', views.contentComment, name='contentComment'),
    path('addContentComment/<int:id>', views.addContentComment, name='addContentComment'),
    path('deletecomment/<int:id>', views.deletecomment, name='deletecomment'),

    path('allcomments/', views.allcomments, name='allcomments'),
    path('adminnotacceptcomment/<int:id>', views.adminnotacceptcomment, name='adminnotacceptcomment'),
    path('adminacceptcomment/<int:id>', views.adminacceptcomment, name='adminacceptcomment'),
    path('admindeletecomment/<int:id>', views.admindeletecomment, name='admindeletecomment'),


    

    
]
