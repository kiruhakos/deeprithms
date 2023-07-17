"""
URL configuration for aiplace project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings
from djoser.views import TokenCreateView, TokenDestroyView
from django.conf.urls.i18n import i18n_patterns


urlpatterns = [
    path('', include('main.urls')),
    path('admin/', admin.site.urls),
    path('api/auth/', include('rest_framework.urls')),
    path('auth/token/', TokenCreateView.as_view(), name='api_token_auth'),
    path('auth/token/destroy/', TokenDestroyView.as_view(), name='api_token_destroy'), 
    path('', include('allauth.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')), 
    path("pages/", include("django.contrib.flatpages.urls")),
    path('i18n/', include('django.conf.urls.i18n')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += i18n_patterns(
    path('pages/', include('django.contrib.flatpages.urls')),
    path("", include("main.urls")),
)


