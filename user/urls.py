from django.urls import path

from . import views

urlpatterns = [
       path('', views.index, name='index'),
       path('update/', views.user_update, name='user_update'),
       path('<int:id>/password', views.change_password, name='change_password'),
       path('comments/', views.comments, name='comments'),
       path('deletecomment/<int:id>', views.deletecomment, name='deletecomment'),
       path('admindeletecomment/<int:id>', views.admindeletecomment, name='admindeletecomment'),

       path('addcontent/', views.addcontent, name='addcontent'),
       path('contents/', views.contents, name='contents'),
       path('notes/', views.notes, name='notes'),
       path('addnotes/', views.addnotes, name='addnotes'),
       path('updatenotes/<int:id>', views.updatenotes, name='updatenotes'),
       path('deletenotes/<int:id>', views.deletenotes, name='deletenotes'),
       path('addimages/<int:id>', views.addimages, name='addimages'),
       path('deletenotesimage/<int:id>', views.deletenotesimage, name='deletenotesimage'),
       path('addshare/<int:id>', views.addshare, name='addshare'),
       path('notshare/<int:id>', views.notshare, name='notshare'),

       path('adminaddshare/<int:id>', views.adminaddshare, name='adminaddshare'),
       path('adminnotshare/<int:id>', views.adminnotshare, name='adminnotshare'),

       path('adminaccept/<int:id>', views.adminaccept, name='adminaccept'),
       path('adminnotaccept/<int:id>', views.adminnotaccept, name='adminnotaccept'),
       path('admindeletenotes/<int:id>', views.admindeletenotes, name='admindeletenotes'),
       path('adminupdatenotes/<int:id>', views.adminupdatenotes, name='adminupdatenotes'),
       path('allcomments/', views.allcomments, name='allcomments'),
       
       path('adminnotcommentaccept/<int:id>', views.adminnotcommentaccept, name='adminnotcommentaccept'),
       path('admincommentaccept/<int:id>', views.admincommentaccept, name='admincommentaccept'),

       path('allcontent/', views.allcontent, name='allcontent'),

       path('addcontent/', views.addcontent, name='addcontent'),
       path('contentedit/<int:id>', views.contentedit, name='contentedit'),
       path('deletecontent/<int:id>', views.deletecontent, name='deletecontent'),
       
       path('adminnotcontentaccept/<int:id>', views.adminnotcontentaccept, name='adminnotcontentaccept'),
       path('admincontentaccept/<int:id>', views.admincontentaccept, name='admincontentaccept'),
       path('admincontentedit/<int:id>', views.admincontentedit, name='admincontentedit'),
       path('admindeletecontent/<int:id>', views.admindeletecontent, name='admindeletecontent'),

       path('addgalimage/<int:id>', views.addgalimage, name='addgalimage'),
       path('deletegalimage/<int:id>', views.deletegalimage, name='deletegalimage'),

       path('admin/', views.admin, name='admin'),
       path('allnotes/', views.allnotes, name='allnotes'),
       path('users/', views.users, name='users'),

       path('deleteusers/<int:id>', views.deleteusers, name='deleteusers'),
       

   ]
