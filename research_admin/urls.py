from django.contrib import admin
from django.urls import path, include
from django.conf import settings

# Customize admin site
admin.site.site_header = getattr(settings, 'ADMIN_SITE_HEADER', 'Research Admin')
admin.site.site_title = getattr(settings, 'ADMIN_SITE_TITLE', 'CvLAC and GrupLAC Integration')
admin.site.index_title = getattr(settings, 'ADMIN_INDEX_TITLE', 'Research Management')

urlpatterns = [
    path('admin/', admin.site.urls),
    # You can add more URL patterns for your apps here
]

# Add a custom admin index view
from django.shortcuts import redirect

# Redirect root URL to admin page
urlpatterns += [
    path('', lambda request: redirect('admin:index'), name='index'),
]