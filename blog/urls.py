from django.urls import path
from . import views
app_name = 'blog'
urlpatterns = [
 path('', views.home, name='home'), path('explore/', views.explore, name='explore'), path('about/', views.about, name='about'),
 path('categories/', views.categories, name='categories'), path('category/<slug:slug>/', views.category, name='category'), path('search/', views.search, name='search'), path('dashboard/', views.dashboard, name='dashboard'),
 path('create-post/', views.post_create, name='post_create'), path('post/<slug:slug>/', views.post_detail, name='post_detail'), path('post/<slug:slug>/edit/', views.post_edit, name='post_edit'), path('post/<slug:slug>/delete/', views.post_delete, name='post_delete'),
 path('post/<slug:slug>/comment/', views.comment_create, name='comment_create'), path('comment/<int:pk>/delete/', views.comment_delete, name='comment_delete'),
]
