"""
URL configuration for pizza_ordering project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from home.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('signup/', register, name='register'),
    path('login/', login, name='login'),
    path('add_cart/<uuid:pizza_uid>/', add_cart, name='add_cart'),
    path('cart/', cart, name='cart'),
    path('order/',order,name='order'),
    path('remove_cart_items/<uuid:cart_item_uid>/',remove_cart_items,name='remove_cart_items'),
    path('increase_quantity/<uuid:cart_item_uid>/', increase_quantity, name='increase_quantity'),
    path('decrease_quantity/<uuid:cart_item_uid>/', decrease_quantity, name='decrease_quantity'),
]
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)


urlpatterns += staticfiles_urlpatterns()