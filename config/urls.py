from django.contrib import admin
from django.urls import path, include
from soso import views
from django.views.generic import RedirectView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("soso/", include("soso.urls")),
    
    path("", RedirectView.as_view(url="/soso/main/")),
]