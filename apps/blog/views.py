from django.shortcuts import render
from rest_framework.generics import ListAPIView, RetrieveAPIView
from .models import Post, Category
from .serializers import PostSerializer, PostListSerializer, CategorySerializer

# Create your views here.
class PostListView(ListAPIView):
    queryset = Post.postObject.all()
    serializer_class = PostListSerializer

class PostDetailView(RetrieveAPIView):
    queryset = Post.postObject.all()
    serializer_class = PostSerializer
    lookup_field = 'slug'

'''class CategoryListView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer'''
