from django.contrib import admin
from django.urls import path, include
from soso import views
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("admin/", admin.site.urls),
    path("soso/", include("soso.urls")),
    
    path("", RedirectView.as_view(url="/soso/main/")),
]


# ★ 開発環境でアップロード画像を配信する
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
