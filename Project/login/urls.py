from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views

from . import views
from login.views.login import CustomLoginView

from .views import CustomPasswordResetConfirmView

urlpatterns = [
	path("login/", CustomLoginView.as_view(), name="login"),
	path("logout/", LogoutView.as_view(next_page="index"), name="logout"),
	path('register/', views.register, name='register'),
	path('users/<int:user_id>/settings/deactivate', views.deactivate_account, name='deactivate_account'),
	
	# Handling emails for Password Reset
	path('password_reset/', views.custom_password_reset, name='password_reset'),
	path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
	
	# Activating account after first registration
	path('activate/<uidb64>/<token>/', views.activate_account, name='activate'),
	
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
