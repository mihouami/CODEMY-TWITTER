from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from schema_graph.views import Schema

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("musker.urls")),
    path("", include("users.urls")),
    # SCHEMA
    path("schema/", Schema.as_view()),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
