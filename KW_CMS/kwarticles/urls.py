from django.contrib import admin
from django.urls import path
from django.urls import include
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name ='kwarticles'

urlpatterns = [
    path('main/', views.main_view),
    path('article/<int:a_id>/', views.article_view),
    path('add_article/', views.add_article),
    path('add_comment/<int:article_id>/', views.add_comment),
    path('login/', views.login),
    path('logout/', views.logout_view),
    path('article_edit/<int:a_id>/', views.article_edit),
    path('article_del/<int:a_id>/', views.article_del, name='article_del'),
    path('contact/', views.contact),
    path('article_accept/',views.article_accept),
    path('article_public/<int:a_id>',views.article_play, name='article_public'),
    path('podgląd/<int:a_id>/', views.look),
]