from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import FileResponse, Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from content.models import Menu
from home.models import Settings
from notes.models import Category, Comment, CommentForm, Notes

# Create your views here.

def index(request):
    text="Merhaba Django <br> <font color='red'> Kemal ŞİMŞEK</font><br>"
    context={'text': text}
    return render(request, 'index.html', context)

@login_required(login_url='login')
def addcomment(request,id):
   url = request.META.get('HTTP_REFERER') 

   if request.method == 'POST':  
      form = CommentForm(request.POST)
      if form.is_valid():
         data = Comment()
         data.subject = form.cleaned_data['subject']
         data.comment = form.cleaned_data['comment']
         data.rate = form.cleaned_data['rate']
         data.ip = request.META.get('REMOTE_ADDR')
         data.note_id=id
         current_user= request.user
         data.user_id=current_user.id
         data.save()
         messages.success(request, "Yorumunuz başarılı bir şekilde eklendi!")
         return HttpResponseRedirect(url)
      messages.warning(request, "Yorumunuz kaydedilmedi! Lütfen bilgilerinizi kontrol ediniz!")
   return HttpResponseRedirect(url)

@login_required(login_url='login')
def pdf_view(request,id):
   pdf=Notes.objects.get(id=id)
   category=Category.objects.all()
   menu=Menu.objects.all()
   settings=Settings.objects.get(pk=1)
   url=pdf.filePdf.url

   context= {
      'category': category,
      'menu': menu,
      'settings': settings,
      'url': url,
      'pdf': pdf,
   }
   return render(request, 'pdf_viewer.html', context)

  