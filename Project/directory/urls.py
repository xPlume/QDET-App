from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView

from . import views

urlpatterns = [
	path("", views.index, name="index"),
	path("create/", views.create, name="create"),
	path("upload/", views.upload_csv, name="upload_csv"),
	path("logout/", LogoutView.as_view(next_page="index"), name="logout"),
	
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)