from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from home.models import Settings
from content.models import Menu
from notes.models import Category 

from notecart.models import NoteCart, NoteCartForm

# Create your views here.
def index (request):
    return HttpResponse("<center><h2>NoteCard App</h2></center>")

@login_required(login_url='/login')
def addtocart(request,id):
    url=request.META.get('HTTP_REFERER')
    current_user=request.user
    kontrol=NoteCart.objects.filter(note_id=id, user=current_user)
    if kontrol:
        messages.success(request, "Listede zaten var..")
        return HttpResponseRedirect(url)
    else:
        if request.method == 'POST':
            form=NoteCartForm(request.POST)
            if form.is_valid():
                data=NoteCart()
                quantity=1
                data.note_id=id
                data.user_id=current_user.id
                data.quantity=quantity
                data.save()
                request.session['cart_item']=NoteCart.objects.filter(user_id=current_user.id).count()
                messages.success(request, "Eklendi")
                return HttpResponseRedirect(url)

    request.session['cart_item']=NoteCart.objects.filter(user_id=current_user.id).count()
    messages.warning(request, "Hata oluştu!")
    return HttpResponseRedirect(url)

@login_required(login_url='/login')
def deletefromcart(request,id):
    NoteCart.objects.filter(id=id).delete()
    current_user=request.user
    request.session['cart_item']=NoteCart.objects.filter(user_id=current_user.id).count()
    messages.success(request, "Beğeni Listesinden Not Silindi!")
    return HttpResponseRedirect('/notelist/')

def notelist(request):
    category=Category.objects.all()
    settings=Settings.objects.get(pk=1)
    menu=Menu.objects.all()
    current_user=request.user
    notecart=NoteCart.objects.filter(user_id=current_user.id)
    request.session['cart_item']=NoteCart.objects.filter(user_id=current_user.id).count()
    context= {
        'category': category,
        'notecart': notecart,
        'settings': settings,
        'menu': menu,
    }

    return render(request, 'notecart.html', context)