from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView

from . import views

urlpatterns = [
	path("", views.index, name="index"),
	path("new_context/", views.new_context, name="new_context"),
	path("new_question/<int:context_id>", views.new_question, name="new_question"),
	path("upload/", views.upload_csv, name="upload_csv"),
	path("questions/", views.user_questions, name="user_questions"),
	path("questions/<int:question_id>", views.single_question, name="single_question"),
	path("questions/<int:question_id>/update", views.update_question, name="update_question"),
	
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)