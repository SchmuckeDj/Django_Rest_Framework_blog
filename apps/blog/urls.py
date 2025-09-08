from django.urls import path
from .views import PostListView, PostDetailView, PostHeadingsView #, CategoryListView

urlpatterns = [
    path('posts/', PostListView.as_view(), name='post-list'),
    path('posts/<slug>/', PostDetailView.as_view(), name='post-detail'),
    path('posts/<slug>/headings/', PostHeadingsView.as_view(), name='post-headings'),
    #path('categories/', CategoryListView.as_view(), name='category-list'),
]