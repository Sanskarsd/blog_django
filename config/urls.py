from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path
from blog.sitemaps import PostSitemap
from blog import views

sitemaps = {'posts': PostSitemap}
urlpatterns = [
    path('admin/', admin.site.urls), path('', include('blog.urls')),
    path('accounts/', include('accounts.urls')), path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='sitemap'),
    path('robots.txt', views.robots, name='robots'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
handler400 = 'blog.views.error_400'
handler403 = 'blog.views.error_403'
handler404 = 'blog.views.error_404'
handler500 = 'blog.views.error_500'
