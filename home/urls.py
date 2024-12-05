from django.urls import path
from . import views

app_name = 'home'
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('post_detail/<int:post_id>/<slug:post_slug>/', views.PostDetailView.as_view(), name='post_detail'),
    path('post_edit/<int:post_id>/', views.PostEditView.as_view(), name='post_edit'),
    path('post_delete/<int:post_id>/', views.PostDeleteView.as_view(), name='post_delete'),
    path('post_create/', views.PostCreateView.as_view(), name='post_create'),
    # path('reply/<int:post_id>/<int:comment_id>/', views.PostAddReplyView.as_view(), name='add_reply'),
    path('post/<int:post_id>/<slug:post_slug>/like/', views.LikePostView.as_view(), name='post_like'),


    ]