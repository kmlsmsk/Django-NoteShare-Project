
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from notecart import views as notecartviews
from user import views as usserviews

from home import views

urlpatterns = [
    path('', include('home.urls')),
    path('home/', include('home.urls')),
    path('admin/', admin.site.urls),
    path('notes/', include('notes.urls')),
    path('user/', include('user.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('notecart/', include('notecart.urls')),
    path('content/', include('content.urls')),
    path('curriculumVitae/', include('curriculumVitae.urls')),

    path('contact/', views.contact, name='contact'),  #Eklenen satır: ilişkilendirme
    path('aboutus/', views.aboutus, name='aboutus'),
    path('cv/', views.cv, name='cv'),
    path('references/', views.references, name='references'),
    path('error/', views.error, name='error'),

    path('category/<int:id>/<slug:slug>/', views.category_notes, name='category_notes'),
    path('notes/<int:id>/<slug:slug>/', views.note_details, name='note_details'),
    path('comments/<int:id>/<slug:slug>/', views.comment, name='comment'),
    path('content/<int:id>/<slug:slug>/', views.content_detail, name='content_detail'),
    path('contents/<int:id>/<slug:slug>/', views.contentdetail, name='contentdetail'),

    path('note_search/', views.note_search, name='note_search'),
    path('note_search_auto/', views.note_search_auto, name='note_search_auto'),
    path('logout/', views.logout_view, name='logout_view'),
    path('login/', views.login_view, name='login_view'),
    path('signup/', views.signup_view, name='signup_view'),
    path('faq/', views.faq, name='faq'),
    path('notelist/', notecartviews.notelist, name='notelist'),
    path('<int:id>/password/', usserviews.change_password, name='change_password'),
    path('menu/<int:id>', views.menu, name='menu'),


]

if settings.DEBUG: #Eklenen kısım
    urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

