from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from home.models import FAQ, Settings, UserProfile
from django.contrib import messages   
from home.models import ContactForm, ContactFormMessage, Settings
from home.forms import SearchForm, SignUpForm
from content.models import CImages, Content, ContentComment, Menu
from notecart.models import NoteCart
from notes.models import Category, Comment, Images, Notes
from django.contrib.auth import logout, login, authenticate
from django.core.paginator import Paginator
import json

# Create your views here.

def index(request):
    menu=Menu.objects.all()
    category=Category.objects.all()
    current_user=request.user
    settings=Settings.objects.get(pk=1)
    sliderData=Notes.objects.filter(status='True', share='True').order_by('?')[:4]
    dayNotes=Notes.objects.filter(status='True', share='True')[:4]
    lastNotes=Notes.objects.filter(status='True', share='True').order_by('-id')[:10]
    randomNotes=Notes.objects.filter(status='True', share='True').order_by('?')[:3]
    notes=Notes.objects.filter(status='True', share='True')
    request.session['cart_item']=NoteCart.objects.filter(user_id=current_user.id).count()
    request.session['note_item']=Notes.objects.filter(user_id=current_user.id).count()
    request.session['comments_item']=Comment.objects.filter(user_id=current_user.id).count()
    request.session['content_item']=Content.objects.filter(user_id=current_user.id).count()
    request.session['contentcomments_item']=ContentComment.objects.filter(user_id=current_user.id).count()
    
    news=Content.objects.filter(type='haber', status='True').order_by('-id')[:4]
    announcements=Content.objects.filter(type='duyuru', status='True').order_by('-id')[:4]

    context={'settings': settings,
             'category': category,
            'sliderData': sliderData,
            'dayNotes': dayNotes,
            'lastNotes': lastNotes,
            'randomNotes': randomNotes,
            'news': news,
            'announcements': announcements,
            'notes':notes,
            'menu': menu,
            'page': 'home'}
    return render(request, 'index.html', context)

def contact(request):
    if request.method=='POST':
        form=ContactForm(request.POST)
        if form.is_valid():
            data=ContactFormMessage()
            data.name=form.cleaned_data['name']
            data.email=form.cleaned_data['email']
            data.subject=form.cleaned_data['subject']
            data.message=form.cleaned_data['message']
            data.ip=request.META.get('REMOTE_ADDR')

            data.save()
            messages.success(request, "Mesajınız başarılı bir şekilde gönderilmiştir!")
            return HttpResponseRedirect('/contact')

    settings=Settings.objects.get(pk=1)
    category=Category.objects.all()
    menu=Menu.objects.all()
    form=ContactForm
    context={'settings': settings, 
             'category': category,
             'menu': menu,
             'form': form}
    
    return render(request, 'contact.html', context)

def aboutus(request):
    settings=Settings.objects.get(pk=1)
    category=Category.objects.all()
    menu=Menu.objects.all()
    context={'settings': settings,
             'category': category,
             'menu': menu,
             }
    
    return render(request, 'aboutus.html', context)


def references(request):
    category=Category.objects.all()
    settings=Settings.objects.get(pk=1)
    menu=Menu.objects.all()
    context={'settings': settings,
             'category': category,
             'menu': menu,
             }
    
    return render(request, 'references.html', context)

def category_notes(request, id, slug):
    category=Category.objects.all()
    categoryData=Category.objects.get(pk=id)
    notes=Notes.objects.filter(status='True',category_id=id).order_by('create_at')
    settings=Settings.objects.get(pk=1)
    menu=Menu.objects.all()
    paginator = Paginator(notes, 3)
    page = request.GET.get('page',1)
    page_obj = paginator.page(page)

    context={'notes':notes,
             'category': category,
             'categoryData': categoryData,
             'settings': settings,
             'menu': menu,
             'page_obj': page_obj,
             }
    return render(request, 'notes.html', context)


def note_details(request, id, slug):
    category=Category.objects.all()
    notes=Notes.objects.get(pk=id)
    images=Images.objects.filter(note_id=id)
    
    settings=Settings.objects.get(pk=1)
    menu=Menu.objects.all()
    context={'notes': notes,
             'category': category,
             'images':images,
            
             'settings': settings,
             'menu': menu,
             }
    return render(request, 'notedetails.html', context)


def comment(request, id, slug):
    category=Category.objects.all()
    notes=Notes.objects.get(pk=id)
    images=Images.objects.filter(note_id=id)
    comments=Comment.objects.filter(note_id=id, status='True')
    own_id=notes.user.id
    profile=UserProfile.objects.get(user_id=own_id)
    menu=Menu.objects.all()
    settings=Settings.objects.get(pk=1)
    context={'notes': notes,
             'category': category,
             'images':images,
             'settings': settings,
             'comments':comments,
             'puan': [1,2,3,4,5], 
             'profile':profile,
             'menu': menu,
             }
    return render(request, 'comments.html', context)

def note_search(request):
    category=Category.objects.all()
    if request.method == 'POST':
        form=SearchForm(request.POST)
        if form.is_valid():
            query=form.cleaned_data['query']
            catid=form.cleaned_data['catid']
            if catid=='a':
                notes=Notes.objects.filter(status='True',title__icontains=query).order_by('create_at')
            else:
                notes=Notes.objects.filter(status='True', title__icontains=query, category_id=catid).order_by('create_at')
    if request.method == 'GET':
        query=request.GET.get('query')
        catid=request.GET.get('catid')
        if catid == 'a':
            notes=Notes.objects.filter(status='True',title__icontains=query).order_by('create_at')
        else:
            notes=Notes.objects.filter(status='True', title__icontains=query, category_id=catid).order_by('create_at')

    paginator = Paginator(notes, 3)
    page = request.GET.get('page',1)
    page_obj = paginator.page(page)

    
    settings=Settings.objects.get(pk=1)
    
    menu=Menu.objects.all()
    context={'category': category,
             'settings': settings,
             'menu': menu,
             'page_obj': page_obj,
             'query': query,
             'catid': catid,
                     }
    return render(request, 'note_search.html', context)
   

def note_search_auto(request):
    if request.is_ajax():
        q = request.GET.get('term', ' ')
        notes = Notes.objects.filter(title__icontains=q)
        results = []
        for rs in notes:
            notes_json = {}
            notes_json = rs.title +" / " + rs.category.title
            results.append(notes_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')


def login_view(request):
    if request.method== 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/')
        else:
            messages.warning(request, "Login Hata!")
            return HttpResponseRedirect('/login')
    settings=Settings.objects.get(pk=1)
    category=Category.objects.all()
    menu=Menu.objects.all()
    context={'category': category,
             'settings': settings,
             'menu': menu,
            
             }
    return render(request, 'login.html', context)

def signup_view(request):
    if request.method == 'POST':
        form=SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username=form.cleaned_data.get('username')
            password=form.cleaned_data.get('password1')
            user=authenticate(username=username,password=password)
            login(request, user)
            current_user=request.user # Eklenen kısım: Otomatik profil oluşturma
            data=UserProfile()
            data.user_id=current_user.id
            data.image="images/users/user.png"
            data.save()
            messages.success(request, "Hoş geldiniz!")
            return HttpResponseRedirect('/')
        
    form= SignUpForm()
    category=Category.objects.all()
    menu=Menu.objects.all()
    settings=Settings.objects.get(pk=1)
    context= {'category': category,
              'menu': menu,
              'form': form,
              'settings': settings,
              }
    return render(request, 'signup.html', context)

def content_detail(request):

   notes=Notes.objects.filter(status='True',category_id=id)
   link='/notes/'+str(notes[0].id+'/'+notes[0].slug)
   return HttpResponseRedirect(link)

def cv(request):
    settings=Settings.objects.get(pk=1)

    context={
        'settings': settings,

    }
    
    return render(request, 'cv.html', context)


def faq(request):
    category=Category.objects.all()
    settings=Settings.objects.get(pk=1)
    faq=FAQ.objects.all().order_by('number')
    menu=Menu.objects.all()
    context= {
        'category': category,
        'faq': faq,
        'settings': settings,
        'menu': menu,
    }
    return render(request, 'faq.html', context)

def menu(request, id):
    try: 
        content=Content.objects.get(menu_id=id)
        link='/contents/'+str(content.id)+'/menu'
        return HttpResponseRedirect(link)
    except:
        link='/error'
        return HttpResponseRedirect(link)
    
def error(request):
    category=Category.objects.all()
    menu=Menu.objects.all()
    settings=Settings.objects.get(pk=1)
    context={
        'category': category,
        'menu': menu,
        'settings': settings,
    }
    return render(request, 'error.html', context)

def contentdetail(request,id, slug):
    category=Category.objects.all()
    menu=Menu.objects.all()
    settings=Settings.objects.get(pk=1)
    content=Content.objects.get(pk=id)
    images=CImages.objects.filter(content_id=id)
    context= {
        'content': content,
        'category': category,
        'menu': menu,
        'images': images,
        'settings': settings,
    }
    return render(request, 'content_detail.html', context)