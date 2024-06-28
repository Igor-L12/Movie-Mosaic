"""acme_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView

from django.urls import include, path, reverse_lazy

urlpatterns = [    
    # Если на сервер пришёл запрос к главной странице,
    # Django проверит на совпадение с запрошенным URL 
    # все path() в файле urls.py приложения homepage.

    # Если в приложении homepage не найдётся совпадений,
    # Django продолжит искать совпадения здесь, в корневом файле urls.py.

    # Если запрос начинается с catalog/, 
    # Django будет искать совпадения в файле urls.py
    # приложения catalog.
    path('catalog/', include('catalog.urls')),
    path('grappelli/', include('grappelli.urls')),
    path('admin/', admin.site.urls),
    path('auth/', include('django.contrib.auth.urls')),
    path(
        'auth/registration/', 
        CreateView.as_view(
            template_name='registration/registration_form.html',
            form_class=UserCreationForm,
            success_url=reverse_lazy('homepage:index'),
        ),
        name='registration',
    ),
    path('', include('posts.urls')),
    path('', include('homepage.urls')),
    path('games/', include('games.urls', namespace='games')),
    path('serials/', include('serials.urls', namespace='serials')),
    path("select2/", include("django_select2.urls")),
] 


if settings.DEBUG:
    import debug_toolbar
    # Добавить к списку urlpatterns список адресов из приложения debug_toolbar:
    urlpatterns += (path('__debug__/', include(debug_toolbar.urls)),) 
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )