from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from home.models import Settings, UserProfile
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from content.models import AdminContentForm, CImages, Content, ContentForm, ContentImageForm, Menu
from user.forms import ProfileUpdateForm, UserUpdateForm
from django.contrib import messages 
from notes.models import AdminNotesForm, Category, Comment, Images, Notes, NotesForm, NotesImageForm

# Create your views here.

def index (request):
    category=Category.objects.all()
    menu=Menu.objects.all()
    current_user=request.user
    settings=Settings.objects.get(pk=1)
    profile=UserProfile.objects.get(user_id=current_user.id)
    
    context={'category': category,
             'profile': profile,
             'menu': menu,
             'settings': settings,
             }
    return render(request, 'user_profile.html', context)

@login_required(login_url='/login')
def user_update(request):
    if request.method == 'POST':
        user_form=UserUpdateForm(request.POST, instance=request.user)
        profile_form=ProfileUpdateForm(request.POST, request.FILES, instance=request.user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Profiliniz Güncellendi!")
            return redirect ('/user')

    else:
        category=Category.objects.all()
        menu=Menu.objects.all()
        settings=Settings.objects.get(pk=1)
        user_form=UserUpdateForm(instance=request.user)
        profile_form=ProfileUpdateForm(instance=request.user.userprofile)
        context={
            'category': category,
            'user_form': user_form,
            'profile_form': profile_form,
            'menu': menu,
            'settings': settings,
        }
        
    return render (request, 'user_update.html', context)

@login_required(login_url='/login')
def change_password (request, id):
    if request.method == 'POST':
        form=PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user=form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Şifreniz Değiştirildi!")
            return HttpResponseRedirect('/user')
        else:
            messages.error(request, "Hatalı işlem! <br>"+str(form.errors))
            return HttpResponseRedirect('/user/'+str(id)+'/password')
    else:
        category=Category.objects.all()
        menu=Menu.objects.all()
        form=PasswordChangeForm(request.user)
        settings=Settings.objects.get(pk=1)
        return render (request, 'change_password.html', {
            'form': form,
            'category': category,
            'menu': menu,
            'settings': settings,
        })

@login_required(login_url='/login')   
def comments(request):
    settings=Settings.objects.get(pk=1)
    menu=Menu.objects.all()
    category=Category.objects.all()
    current_user=request.user
    comments=Comment.objects.filter(user_id=current_user.id)
    request.session['comments_item']=Comment.objects.filter(user_id=current_user.id).count()
    context= {
        'category': category,
        'comments': comments,
        'settings': settings,
        'menu': menu,
    }

    return render(request, 'user_comments.html', context)


@login_required(login_url='/login')   
def allcomments(request):
    settings=Settings.objects.get(pk=1)
    menu=Menu.objects.all()
    category=Category.objects.all()
    comments=Comment.objects.filter()
    context= {
        'category': category,
        'comments': comments,
        'settings': settings,
        'menu': menu,
    }

    return render(request, 'admin_comments.html', context)

@login_required(login_url='/login')
def deletecomment(request, id):
    current_user=request.user
    Comment.objects.filter(id=id, user_id=current_user.id).delete()
    messages.success(request, 'Yorum Silindi...')
    return HttpResponseRedirect('/user/comments')

@login_required(login_url='/login')
def admindeletecomment(request, id):
    
    Comment.objects.filter(id=id).delete()
    messages.success(request, 'Yorum silindi!')
    return HttpResponseRedirect('/user/allcomments')


@login_required(login_url='/login')
def contents(request):
    category=Category.objects.all()
    menu=Menu.objects.all()
    settings=Settings.objects.get(pk=1)
    current_user=request.user
    contents=Content.objects.filter(user_id=current_user.id)
    request.session['content_item']=Content.objects.filter(user_id=current_user.id).count()
    context={
        'category': category,
        'menu': menu,
        'contents': contents,
        'settings': settings,
    }
    return render(request, 'user_contents.html', context)

@login_required(login_url='/login')
def addcontent(request):
    if request.method=='POST':
        form=ContentForm(request.POST, request.FILES)
        if form.is_valid():
            current_user=request.user
            data=Content()
            data.user_id=current_user.id
            data.title=form.cleaned_data['title']
            data.keywords=form.cleaned_data['keywords']
            data.description=form.cleaned_data['description']
            data.image=form.cleaned_data['image']
            data.type=form.cleaned_data['type']
            
            data.detail=form.cleaned_data['detail']
            data.status='False'
            data.save()
            messages.success(request, "İçerik Kaydedildi!")
            return HttpResponseRedirect('/user/contents')
        else:
            messages.warning(request, 'Hatalı Giriş: ' +str(form.errors))
            return HttpResponseRedirect('/user/addcontent')
    else:
        category=Category.objects.all()
        menu=Menu.objects.all()
        settings=Settings.objects.get(pk=1)
        form=ContentForm()
        durum=0
        context= {
            'category': category,
            'menu': menu,
            'form': form,
            'settings': settings,
            'durum': durum,
        }
    return render(request, 'user_addcontent.html', context)

@login_required(login_url='/login')
def deletecontent(request, id):
    current_user=request.user
    Content.objects.filter(id=id, user_id=current_user.id).delete()
    messages.success(request, 'İçerik Silindi...')
    return HttpResponseRedirect('/user/contents')

@login_required(login_url='/login')
def contentedit(request, id):
    content=Content.objects.get(id=id)
    if request.method=='POST':
        form=ContentForm(request.POST, request.FILES, instance=content)
        if form.is_valid():
            form.save()
            messages.success(request, "İçerik Güncellendi!")
            return HttpResponseRedirect('/user/contents')
        else:
            messages.warning(request, "Hatalı İşlem: "+str(form.errors))
            return HttpResponseRedirect('/user/contentedit/'+str(id))
    else:
        category=Category.objects.all()
        menu=Menu.objects.all()
        settings=Settings.objects.get(pk=1)
        form=ContentForm(instance=content)
        durum=1
        context= {
            'category': category,
            'menu':menu,
            'form': form,
            'settings': settings,
            'durum': durum,
        }
        return render(request, 'user_addcontent.html', context)
    
@login_required(login_url='/login')
def addgalimage(request, id):
    if request.method=='POST':
        lasturl=request.META.get('HTTP_REFERER')
        form=ContentImageForm(request.POST, request.FILES)
        if form.is_valid():
            data=CImages()
            data.title=form.cleaned_data['title']
            data.content_id=id
            data.image=form.cleaned_data['image']
            data.save()
            messages.success(request,'Resim Yüklendi...')
            return HttpResponseRedirect(lasturl)
        else:
            messages.warning(request, 'Hata var : '+str(form.errors))
            return HttpResponseRedirect(lasturl)
    else:
        content=Content.objects.get(id=id)
        images=CImages.objects.filter(content_id=id)
        form=ContentImageForm()
        context= {
            'content': content,
            'images': images,
            'form': form,
        }
        return render(request, 'content_gallery.html', context)
    
@login_required(login_url='/login')
def deletegalimage (request, id):
    lasturl=request.META.get('HTTP_REFERER')
    
    CImages.objects.filter(id=id).delete()
    messages.success(request, 'Resim Silindi...')
    return HttpResponseRedirect(lasturl)


@login_required(login_url='/login')
def notes (request):
    current_user=request.user
    category=Category.objects.all()
    settings=Settings.objects.get(pk=1)
    menu=Menu.objects.all()
    notes=Notes.objects.filter(user_id=current_user.id)
    
    context= {
        'category': category,
        'settings': settings,
        'menu': menu,
        'notes': notes,
        }
    return render(request, 'user_notes.html', context)

@login_required(login_url='/login')
def addnotes (request):
    if request.method=='POST':
        form=NotesForm(request.POST, request.FILES)
        if form.is_valid():
            current_user=request.user
            data=Notes()
            data.user_id=current_user.id
            data.title=form.cleaned_data['title']
            data.category=form.cleaned_data['category']
            data.keywords=form.cleaned_data['keywords']
            data.description=form.cleaned_data['description']
            data.image=form.cleaned_data['image']
            data.filePdf=form.cleaned_data['filePdf']
            
            data.detail=form.cleaned_data['detail']
            data.status='False'
            data.share='False'
            data.save()
            messages.success(request, "Not başarılı bir şekilde kaydedildi!")
            return HttpResponseRedirect('/user/notes')
        else:
            messages.warning(request, 'Hatalı Giriş: ' +str(form.errors))
            return HttpResponseRedirect('/user/addnotes')
        
    else:
        current_user=request.user
        category=Category.objects.all()
        settings=Settings.objects.get(pk=1)
        menu=Menu.objects.all()
        notes=Notes.objects.filter(user_id=current_user.id)
        durum=0
        form=NotesForm()
        context= {
            'category': category,
            'menu': menu,
            'form': form,
            'notes': notes,
            'durum': durum,
            'settings': settings,
        }
        return render(request, 'user_addnotes.html', context)
    

@login_required(login_url='/login')
def updatenotes(request, id):
    notes=Notes.objects.get(id=id)
    if request.method=='POST':
        form=NotesForm(request.POST, request.FILES, instance=notes)
        if form.is_valid():
            form.save()
            messages.success(request, "Not İçeriği Güncellendi!")
            return HttpResponseRedirect('/user/notes')
        else:
            messages.warning(request, "Hatalı İşlem: "+str(form.errors))
            return HttpResponseRedirect('/user/uptadenotes/'+str(id))
    else:
        category=Category.objects.all()
        settings=Settings.objects.get(pk=1)
        menu=Menu.objects.all()
        form=NotesForm(instance=notes)
        durum=1
        context= {
            'category': category,
            'menu':menu,
            'form': form,
            'durum': durum,
            'settings': settings,
        }
        return render(request, 'user_addnotes.html', context)
    
@login_required(login_url='/login')
def deletenotes(request, id):
    current_user=request.user
    Notes.objects.filter(id=id, user_id=current_user.id).delete()
    messages.success(request, 'Not İçeriği Silindi...')
    return HttpResponseRedirect('/user/notes/')



@login_required(login_url='/login')
def addimages(request, id):
    if request.method=='POST':
        lasturl=request.META.get('HTTP_REFERER')
        form=NotesImageForm(request.POST, request.FILES)
        if form.is_valid():
            data=Images()
            data.title=form.cleaned_data['title']
            data.note_id=id
            data.image=form.cleaned_data['image']
            data.save()
            messages.success(request,'Resim Yüklendi...')
            return HttpResponseRedirect(lasturl)
        else:
            messages.warning(request, 'Hata var : '+str(form.errors))
            return HttpResponseRedirect(lasturl)
    else:
        notes=Notes.objects.get(id=id)
        images=Images.objects.filter(note_id=id)
        form=NotesImageForm()
        context= {
            'notes': notes,
            'images': images,
            'form': form,
        }
        return render(request, 'notes_images.html', context)
    

@login_required(login_url='/login')
def deletenotesimage (request, id):
    lasturl=request.META.get('HTTP_REFERER')
    current_user=request.user
    Images.objects.filter(id=id).delete()
    messages.success(request, 'Resim Silindi...')
    return HttpResponseRedirect(lasturl)

@login_required(login_url='/login')
def addshare(request, id):
    Notes.objects.filter(id=id).update(share='True')
    
    return HttpResponseRedirect('/user/notes/')

@login_required(login_url='/login')
def notshare(request, id):
    Notes.objects.filter(id=id).update(share='False')

    return HttpResponseRedirect('/user/notes/')


def admin (request):
    category=Category.objects.all()
    menu=Menu.objects.all()
    current_user=request.user
    settings=Settings.objects.get(pk=1)
    profile=UserProfile.objects.get(user_id=current_user.id)
    
    context={'category': category,
             'profile': profile,
             'menu': menu,
             'settings': settings,
             }
    return render(request, 'user_admin.html', context)

def users(request):
    category=Category.objects.all()
    menu=Menu.objects.all()
    settings=Settings.objects.get(pk=1)
    users=UserProfile.objects.all()
    
    context={'category': category,
             'users': users,
             'menu': menu,
             'settings': settings,
             }
    return render(request, 'user_users.html', context)


@login_required(login_url='/login')
def allnotes (request):
    category=Category.objects.all()
    settings=Settings.objects.get(pk=1)
    menu=Menu.objects.all()
    notes=Notes.objects.all()
    
    context= {
        'category': category,
        'settings': settings,
        'menu': menu,
        'notes': notes,
        }
    return render(request, 'allnotes.html', context)


@login_required(login_url='/login')
def adminaddshare(request, id):
    Notes.objects.filter(id=id).update(share='True')
    
    return HttpResponseRedirect('/user/allnotes/')

@login_required(login_url='/login')
def adminnotshare(request, id):
    Notes.objects.filter(id=id).update(share='False')

    return HttpResponseRedirect('/user/allnotes/')


@login_required(login_url='/login')
def adminaccept(request, id):
    Notes.objects.filter(id=id).update(status='True')
    
    return HttpResponseRedirect('/user/allnotes/')

@login_required(login_url='/login')
def adminnotaccept(request, id):
    Notes.objects.filter(id=id).update(status='False')

    return HttpResponseRedirect('/user/allnotes/')



@login_required(login_url='/login')
def admindeletenotes (request, id):
    
    Notes.objects.filter(id=id).delete()
    messages.success(request, 'Not İçeriği Silindi...')
    return HttpResponseRedirect('/user/allnotes/')


@login_required(login_url='/login')
def adminupdatenotes(request, id):
    notes=Notes.objects.get(id=id)
    if request.method=='POST':
        form=AdminNotesForm(request.POST, request.FILES, instance=notes)
        if form.is_valid():
            form.save()
            messages.success(request, "Not İçeriği Güncellendi!")
            return HttpResponseRedirect('/user/allnotes')
        else:
            messages.warning(request, "Hatalı İşlem: "+str(form.errors))
            return HttpResponseRedirect('/user/adminupdatenotes/'+str(id))
    else:
        category=Category.objects.all()
        settings=Settings.objects.get(pk=1)
        menu=Menu.objects.all()
        form=AdminNotesForm(instance=notes)
        durum=1
        context= {
            'category': category,
            'menu':menu,
            'form': form,
            'durum': durum,
            'settings': settings,
        }
        return render(request, 'admin_addnotes.html', context)
    

@login_required(login_url='/login')
def admincommentaccept(request, id):

    Comment.objects.filter(id=id).update(status='True')
    
    return HttpResponseRedirect('/user/allcomments/')

@login_required(login_url='/login')
def adminnotcommentaccept(request, id):

    Comment.objects.filter(id=id).update(status='False')

    return HttpResponseRedirect('/user/allcomments/')


@login_required(login_url='/login')
def allcontent(request):
    category=Category.objects.all()
    menu=Menu.objects.all()
    settings=Settings.objects.get(pk=1)
   
    contents=Content.objects.all()

    context={
        'category': category,
        'menu': menu,
        'contents': contents,
        'settings': settings,
    }
    return render(request, 'allcontents.html', context)


@login_required(login_url='/login')
def admincontentaccept (request, id):

    Content.objects.filter(id=id).update(status='True')
    
    return HttpResponseRedirect('/user/allcontent/')

@login_required(login_url='/login')
def adminnotcontentaccept(request, id):

    Content.objects.filter(id=id).update(status='False')

    return HttpResponseRedirect('/user/allcontent/')


@login_required(login_url='/login')
def admincontentedit(request, id):
    content=Content.objects.get(id=id)
    if request.method=='POST':
        form=AdminContentForm(request.POST, request.FILES, instance=content)
        if form.is_valid():
            form.save()
            messages.success(request, "İçerik Güncellendi!")
            return HttpResponseRedirect('/user/allcontent')
        else:
            messages.warning(request, "Hatalı İşlem: "+str(form.errors))
            return HttpResponseRedirect('/user/admincontentedit/'+str(id))
    else:
        category=Category.objects.all()
        menu=Menu.objects.all()
        settings=Settings.objects.get(pk=1)
        form=AdminContentForm(instance=content)
        context= {
            'category': category,
            'menu':menu,
            'form': form,
            'settings': settings,
        }
        return render(request, 'admin_addcontent.html', context)
    

@login_required(login_url='/login')
def admindeletecontent(request, id):
    
    Content.objects.filter(id=id).delete()
    messages.success(request, 'İçerik Silindi...')
    return HttpResponseRedirect('/user/allcontent')


@login_required(login_url='/login')
def deleteusers(request, id):
    UserProfile.objects.filter(id=id).delete()

    messages.success(request, 'Kullanıcı Silindi!')
    return HttpResponseRedirect('/user/users')

