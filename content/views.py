from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages
from content.models import CImages, Content, ContentComment, ContentCommentForm, Menu
from home.models import Settings, UserProfile
from django.contrib.auth.decorators import login_required


from notes.models import Category, Images, Notes

# Create your views here.
def index (request):
    return HttpResponse ("Content App")


def contentComment(request, id):
    category=Category.objects.all()
    content=Content.objects.get(pk=id)
    images=CImages.objects.filter(content_id=id)
    comments=ContentComment.objects.filter(content_id=id, status='True')
    profile=UserProfile.objects.get(user_id=content.user.id)
    menu=Menu.objects.all()
    settings=Settings.objects.get(pk=1)
    context={'content': content,
             'category': category,
             'images':images,
             'settings': settings,
             'comments':comments,
             'puan': [1,2,3,4,5], 
             'profile':profile,
             'menu': menu,
             }
    return render(request, 'contentComments.html', context)


@login_required(login_url='login')
def addContentComment(request,id):
   url = request.META.get('HTTP_REFERER') 

   if request.method == 'POST':  
      form = ContentCommentForm(request.POST)
      if form.is_valid():
         data = ContentComment()
         data.subject = form.cleaned_data['subject']
         data.comment = form.cleaned_data['comment']
         data.rate = form.cleaned_data['rate']
         data.ip = request.META.get('REMOTE_ADDR')
         data.content_id=id
         current_user= request.user
         data.user_id=current_user.id
         data.save()
         messages.success(request, "Yorumunuz eklendi!")
         return HttpResponseRedirect(url)
      messages.warning(request, "Yorumunuz kaydedilmedi!")
   return HttpResponseRedirect(url)

@login_required(login_url='/login')   
def comments(request):
    settings=Settings.objects.get(pk=1)
    menu=Menu.objects.all()
    category=Category.objects.all()
    current_user=request.user
    comments=ContentComment.objects.filter(user_id=current_user.id)
    request.session['contentcomments_item']=ContentComment.objects.filter(user_id=current_user.id).count()
    context= {
        'category': category,
        'comments': comments,
        'settings': settings,
        'menu': menu,
        'current_user': current_user,
    }

    return render(request, 'user_contentcomments.html', context)

@login_required(login_url='/login')
def deletecomment(request, id):
    current_user=request.user
    ContentComment.objects.filter(id=id, user_id=current_user.id).delete()
    messages.success(request, 'Yorum Silindi...')
    return HttpResponseRedirect('/content/comments')


@login_required(login_url='/login')   
def allcomments(request):
    settings=Settings.objects.get(pk=1)
    menu=Menu.objects.all()
    category=Category.objects.all()
    comments=ContentComment.objects.all()
    
    context= {
        'category': category,
        'comments': comments,
        'settings': settings,
        'menu': menu,
        
    }

    return render(request, 'admin_contentcomments.html', context)

@login_required(login_url='/login')
def admindeletecomment(request, id): 
    
    ContentComment.objects.filter(id=id).delete()
    messages.success(request, 'Yorum Silindi...')
    return HttpResponseRedirect('/content/allcomments')


@login_required(login_url='/login')
def adminacceptcomment (request, id):

    ContentComment.objects.filter(id=id).update(status='True')
    
    return HttpResponseRedirect('/content/allcomments/')

@login_required(login_url='/login')
def adminnotacceptcomment(request, id):

    ContentComment.objects.filter(id=id).update(status='False')

    return HttpResponseRedirect('/content/allcomments/')

