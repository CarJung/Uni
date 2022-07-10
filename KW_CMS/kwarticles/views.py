from django.shortcuts import get_object_or_404, render, redirect
from .models import KWarticles, KWComment
from .forms import KWarticleForm, ComentForm, KontaktForm

from django.contrib.auth import authenticate, login as www, logout
from django.contrib import messages

from django.http.response import HttpResponse

from django.contrib.auth.decorators import login_required

from django.db.models import ProtectedError

from django.core.mail import send_mail, BadHeaderError
from django.conf import settings
# Create your views here.

def main_view(request):
    user = request.user
    art = KWarticles.objects.filter(status = True).filter(important = True)
    art_last = KWarticles.objects.filter(status=True).order_by('-pub_data')[:]
    pubilcated = KWarticles.objects.filter(status=True)
    return render(request, 'articles.html', {'login' : user, 'art' : art, 'art_last':art_last, 'publicated':pubilcated})

def article_view(request, a_id):
    pubilcated = KWarticles.objects.filter(status=True)
    user = request.user
    art = KWarticles.objects.get(id=a_id)
    com = KWComment.objects.filter(article_id = a_id)
    return render(request, 'article.html', {'login_user' : user, 'art' : art, 'com': com, 'publicated':pubilcated})

@login_required
def add_article(request):
    user = request.user
    
    if request.method == 'POST':
        form = KWarticleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect ('/articles/main/') 
        else:
            return render(request, 'add_article.html', {'form': form})
    else:
        form = KWarticleForm()
        return render(request, 'add_article.html',{'form': form})
    return render(request, 'add_article.html')

def add_comment(request, article_id):
    art = KWarticles.objects.get(id=article_id)

    if request.method == 'POST':
        cform = ComentForm(request.POST)
        if cform.is_valid():
            c = cform.save(commit=False)
            c.article = art
            c.save()
            return redirect ('/articles/main/')
        else:
            return  render(request, 'add_comment.html',{'form': cform})
    else:
        cform= ComentForm()
        return render(request, 'add_comment.html',{'form': cform, 'art': art})


def login(request):
    if request.method =='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username = username, password = password)
        if user is not None:
            www(request, user)

            return redirect('/articles/add_article/')
        else:
            messages.error(request , 'Niepoprawny login lub hasło')
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    user = request.user
    print(user)
    art = KWarticles.objects.filter(important=True)
    art_last = KWarticles.objects.all().order_by('-pub_data')[:3]
    return render(request, 'articles.html', { 'login' : user, 'art_last' : art_last, 'art' : art})

def article_edit(request, a_id):
    publicated = KWarticles.objects.filter(status=True)
    a_object = get_object_or_404(KWarticles, pk=a_id)
    a_form = KWarticleForm(request.POST or None, instance=a_object)
    if request.method == 'POST':
        if a_form.is_valid():
            a_form.save()
            return redirect ('/articles/main/')
        else:
            return  render(request, 'article_editor.html',{'form': a_form, 'publicated': publicated})
    else:
        return  render(request, 'article_editor.html',{'form': a_form, 'publicated': publicated})


def article_del(request, a_id):
    a_object = KWarticles.objects.get(id = a_id)
    art = KWarticles.objects.filter(important=True)
    art_last = KWarticles.objects.all().order_by('-pub_data')[:3]
    try:
        a_object.delete()
        return redirect ('/articles/main/')
    except ProtectedError:
        return render(request, 'articles.html', { 'art_last' :art_last , 'art' : art, 'error':'Nie mozna usunąć' })

def article_play(request, a_id):
    art = KWarticles.objects.all()
    a_object = KWarticles.objects.get(id = a_id)
    try:
        a_object.status = True
        a_object.save()
        return redirect('/articles/article_accept/')
    except ProtectedError:
        print('Błąd')
        return render(request, 'articles_accept.html', {'error' : 'Nie można zmienić statusu'})
        
    return render(request, 'articles_accept.html', {'art': art})

def contact(request):
    if request.method == 'POST':
        c_form = KontaktForm(request.POST)
        if c_form.is_valid():
            subject = 'Wiadomość z systemu CMS'
            body = {
                'first_name' : c_form.cleaned_data['first_name'],
                'last_name' : c_form.cleaned_data['last_name'],
                'mail' : c_form.cleaned_data['c_mail'],
                'text' : c_form.cleaned_data['text'],
                'klauzula' : 'taki sam tekst dla wszystkich wiadomości',

            }
            message = '\n'.join(body.values())
            try:
                send_mail(subject,message, settings.DEFAULT_FROM_EMAIL, [c_form.cleaned_data['c_mail'], 'jantomek76@gmail.com'])
            except BadHeaderError:
                return HttpResponse('Błąd wiadomości')
            return redirect('/articles/main/')
    c_form = KontaktForm()
    return render(request, 'kontakt.html', {'form':c_form})

def article_accept(request):
    publicated = KWarticles.objects.filter(status=True)
    art = KWarticles.objects.all()
    print(art)
    return render(request, 'articles_accept.html', {'art' : art, 'publicated': publicated})

def look(request, a_id):
    publicated = KWarticles.objects.filter(status=True)
    art = KWarticles.objects.get(id=a_id)
    return render(request, 'podgląd.html', { 'art' : art, 'publicated': publicated})
