from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('stem.urls')),
    path('', include('teacher.urls')),
    path('',include('student.urls')),
    path('',include('authentication.urls')),
    path('error',TemplateView.as_view(template_name='error.html'), name='error')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)