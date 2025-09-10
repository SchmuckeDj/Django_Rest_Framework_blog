from django.urls import path
from .views import (
    PostListView, 
    PostDetailView, 
    PostHeadingsView, 
    IncrementPostClicksView
    )

urlpatterns = [
    path('posts/', PostListView.as_view(), name='post-list'), 
    path('posts/<slug>/', PostDetailView.as_view(), name='post-detail'),
    path('posts/<slug>/headings/', PostHeadingsView.as_view(), name='post-headings'),
    path('posts/<slug>/increment_clicks/', IncrementPostClicksView.as_view(), name='increment-post-clicks'),
    #path('categories/', CategoryListView.as_view(), name='category-list'),
]