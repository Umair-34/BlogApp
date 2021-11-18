import debug_toolbar


from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('accounts/', include('allauth.urls')),
                  path('', include('core.urls')),
                  path('summernote/', include('django_summernote.urls')),
                  path('__debug__/', include(debug_toolbar.urls)),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

