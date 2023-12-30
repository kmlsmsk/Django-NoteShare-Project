from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages 
from django.views.decorators.csrf import csrf_exempt

from curriculumVitae.models import DynamiCV, Education, Experience, Form, ListMail, ListMailForm, MessageForm, Skill
from home.models import ContactForm, ContactFormMessage, Settings, UserProfile
from content.models import Content, Menu
from notes.models import Category, Notes
import json

# Create your views here.

def index(request):
    users=UserProfile.objects.all()
    notes=Notes.objects.filter(user_id=1)
    dcv=DynamiCV.objects.get(pk=1)
    edu=Education.objects.all()
    exp=Experience.objects.all()
    skill=Skill.objects.all()
    
    kn=[]
    for i in set(notes):
        kn.append(i.category)

    knn=set(kn)
    
    context= {'skill': skill,
        'users': users,
        'notes': notes,
        'knn': knn,
        'dcv': dcv,
        'edu': edu,
        'exp': exp,
    }
    return render(request, 'cv.html', context)

def cv(request):
    return HttpResponse("CV")

@csrf_exempt
def sendmessage (request):
    if request.method=='POST':
        form=Form(request.POST)
        if form.is_valid():
            data=MessageForm()
            data.name=form.cleaned_data['name']
            data.email=form.cleaned_data['email']
            data.subject=form.cleaned_data['subject']
            data.message=form.cleaned_data['message']
            data.ip=request.META.get('REMOTE_ADDR')
            data.save()
            messages.success(request, "Mesaj Gönderildi!")
            return HttpResponse("Başarılı")
    else:
        contact=1
        context= {
        'contact': contact,
    }
    return render(request, 'contacts.html', context) 

    


def contentcategory (request):
    notes=Notes.objects.filter(status='True', share='True').order_by('-id')
    kn=[]
    for i in set(notes):
        kn.append(i.category)
    knn=set(kn)
    context= {
        'notes': notes,
        'knn': knn,
    }
    return render(request, 'contentcategory.html', context) 

def news(request):
    news=Content.objects.filter(type='haber', status='True').order_by('-id')[:10]
    announcements=Content.objects.filter(type='duyuru', status='True').order_by('-id')[:10]
    context= {
        'news': news,
        'announcements': announcements,
    }
    return render(request, 'news.html', context)

def contacts(request):
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
            messages.success(request, "Mesajınız Gönderildi!")
            return HttpResponseRedirect('/curriculumVitae/contacts/')
    else:
        form=0
        context={
             'form': form,
             }
        return render(request, 'contacts.html', context)
    

def search(request):
    category=Category.objects.all()
    context= {
        'category': category,
    }
    return render(request, 'x_search.html', context) 



def search_auto(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        notes = Notes.objects.filter(title__icontains=q)

        results = []
        print(q)
        for rs in notes:
            notes_json = {}
            notes_json = rs.title
        results.append(notes_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)

def addlistmail(request):
    if request.method=='POST':
        lasturl=request.META.get('HTTP_REFERER')
        
        form=ListMailForm(request.POST)

        if form.is_valid():
            data=ListMail()
            data.email=form.cleaned_data['email']
            data.ip = request.META.get('REMOTE_ADDR')
            if ListMail.objects.filter(email=form.cleaned_data['email']):
                mail=data.email
                category=Category.objects.all()
                menu=Menu.objects.all()
                settings=Settings.objects.get(pk=1)
                return render(request, 'listerror.html', context={'mail':mail, 'category': category, 'menu': menu, 'settings': settings})
            else:
                data.save()
                messages.success(request,'Mail Listesine Eklendi!')
                return HttpResponseRedirect(lasturl)            
        else:
            messages.warning(request, 'Hata var!')
            return HttpResponseRedirect(lasturl)
    else: 
        return HttpResponse("Hata var!")
    
def emaillist(request):
    category=Category.objects.all()
    menu=Menu.objects.all()
    settings=Settings.objects.get(pk=1)
    list=ListMail.objects.all()

    context={
        'list': list,
        'category': category,
        'menu': menu,
        'settings': settings,
    }
    return render(request, 'emaillist.html', context)

def deletemaillist(request, id):
    ListMail.objects.filter(id=id).delete()

    messages.success(request, 'Mail Listeden Silindi...')
    return HttpResponseRedirect('/curriculumVitae/emaillist/')


def skill(request, id):
    skill=Skill.objects.get(id=id)
    context={
        'skill': skill,
    }

    return render(request, 'skill.html', context)
