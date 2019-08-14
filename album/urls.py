from django.contrib import admin
from django.urls import path

from . import views

app_name='album'


urlpatterns = [
    path('', views.homepage, name="homepage"),
    path('pictures/add/', views.PhotoCreateView.as_view(), name="add_photo"),
    path('pictures/<str:author_slug>/<str:slug>-<int:pk>/', views.PhotoDetailView.as_view(), name="detail_photo"),
    path('pictures/<str:author_slug>/<str:slug>-<int:pk>/modify/', views.PhotoUpdateView.as_view(), name="update_photo"),
    path('pictures/<str:author_slug>/<str:slug>-<int:pk>/delete/', views.PhotoDeleteView.as_view(), name="delete_photo"),
    path('pictures/add_comment/', views.AddCommentView, name='add_comment'),
    path('pictures/delete_comment/', views.DeleteCommentView, name='delete_comment'),
    path("search/", views.search_bar_view, name='search_bar'),

]
