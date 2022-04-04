from django.urls import path, include
from . import views
from django.contrib.auth.views import LogoutView
from django.conf import settings
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register('posts', PostViewSet, basename='posts')

urlpatterns=[
    #path('index', views.index, name='blog-main'),
    path("comments/", AddCommentView.as_view()),
    path("comments/<slug:post_slug>/", GetCommentView.as_view()),
    path('register/', RegisterView.as_view()),
    path('profile/', ProfileView.as_view()),
    path("feedback/", FeedbackView.as_view()),
    path("aside/", AsideView.as_view()),
    path("tags/<slug:tag_slug>/", TagDetailView.as_view()),
    path("tags/", TagView.as_view()),
    path("", include(router.urls))
]