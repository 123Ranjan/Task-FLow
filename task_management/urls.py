from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse


def home(request):
    return HttpResponse("Backend Running 🚀")


urlpatterns = [
    path("admin/", admin.site.urls),

    # Your apps - EACH ONLY ONCE!
    path("api/", include("users.urls")),
    path("api/", include("issues.urls")),
    path("api/", include("sprints.urls")),
    path("api/", include("notifications.urls")),
    path("api/ai/", include("ai.urls")),  # ✅ ONLY THIS ONE - with /ai
    path("api/", include("boards.urls")),

    path('', home),
]