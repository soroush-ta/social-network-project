from django.urls import path
from . import views

app_name = 'account'

urlpatterns = [
    path('account/register', views.UserRegisterationView.as_view(), name='register'),
    path('account/login', views.UserLoginView.as_view(), name='login'),
    path('account/logout', views.UserLogoutView.as_view(), name='logout'),
    path('account/profile/<int:user_id>', views.UserProfileView.as_view(), name='profile'),
    path('account/follow/<int:user_id>', views.UserFollowView.as_view(), name='follow'),
    path('account/unfollow/<int:user_id>', views.UserUnfollowView.as_view(), name='unfollow'),
    path('profile/edit/', views.ProfileEditView.as_view(), name='profile_edit'),

]