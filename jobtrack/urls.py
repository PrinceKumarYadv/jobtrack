"""
JobTrack URL configuration.

/                       -> Server-rendered frontend pages (see frontend.urls)
/admin/                 -> Django admin
/api/                   -> Accounts (register/login/logout/profile) + JWT
/api/                   -> Applications, Interviews, Dashboard (DRF routers)
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),

    # REST API
    path("api/", include("accounts.urls")),
    path("api/", include("applications.urls")),
    path("api/", include("interviews.urls")),
    path("api/", include("dashboard.urls")),

    # Server-rendered pages
    path("", include("frontend.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
