from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # API URLs
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    
    # Application URLs
    path('api/accounts/', include('apps.accounts.urls')),
    path("api/courses/", include("apps.courses.urls")),
    path("api/enrollments/", include("apps.enrollments.urls")),
]
