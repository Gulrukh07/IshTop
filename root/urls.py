from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
                  path('ckeditor/', include('ckeditor_uploader.urls')),
                  path('', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
                  path('api/v1/', include('authenticate.urls', namespace='auth')),
                  path('api/v1/', include('apps.urls')),
                  path('api/v1/', include('chat.urls')),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
