from django.urls import path
from notes import views

urlpatterns = [
    path('', views.index, name='index'),
    path('addcomment/<int:id>', views.addcomment, name='addcomment'),
    path('pdf_view/<int:id>', views.pdf_view, name='pdf_view'),
]
