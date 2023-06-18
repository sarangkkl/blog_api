
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from rest_framework import permissions



urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/",include("blog.urls")),
    path("api/accounts/",include("accounts.urls")),

]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

