"""
URL configuration for shuddho_map project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # Landing page
    path('', TemplateView.as_view(template_name='landing.html'), name='landing'),
    
    # Apps
    path('dashboard/', include('dashboard.urls')),
    path('reports/', include('citizen_reports.urls')),
]

# Serve media and static files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # Serve static files from STATICFILES_DIRS
    from django.contrib.staticfiles.views import serve
    from django.urls import re_path
    urlpatterns += [
        re_path(r'^static/(?P<path>.*)$', serve),
    ]

# Admin site customization
admin.site.site_header = "ACTS Administration"
admin.site.site_title = "ACTS Admin"
admin.site.index_title = "Welcome to ACTS Administration"
