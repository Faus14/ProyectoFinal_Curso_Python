from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, LogoutView


urlpatterns = [
	path('', views.feed, name='feed'),
	path('profile/', views.profile, name='profile'),
	path('register/', views.register, name='register'),
	path('login/', LoginView.as_view(template_name='social/login.html'), name='login'),
	path('logout/', LogoutView.as_view(template_name='social/logout.html'), name='logout'),
	path('post/', views.post, name='post'),
	path('follow/<str:username>/', views.follow, name='follow'),
	path('unfollow/<str:username>/', views.unfollow, name='unfollow'),
    path('about/', views.about, name='about'),
    path('comment/<int:post_id>/', views.add_comment, name='add_comment'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('like/<int:post_id>/', views.like_post, name='like_post'),
	
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)