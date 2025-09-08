from django.shortcuts import render
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Post, Category, Heading
from .serializers import PostSerializer, PostListSerializer, CategorySerializer, HeadingSerializer, PostView
from .utils import get_client_ip


# Create your views here.
'''class PostListView(ListAPIView):
    queryset = Post.postObject.all()
    serializer_class = PostListSerializer'''

class PostListView(APIView):
    def get(self, request, *args, **kwargs):
        posts = Post.postObject.all()
        serializer = PostListSerializer(posts, many=True).data
        return Response(serializer)

    
'''class PostDetailView(RetrieveAPIView):
        queryset = Post.postObject.all()
        serializer_class = PostSerializer
        lookup_field = 'slug'''

class PostDetailView(APIView):
    def get(self, request, slug):
        post = Post.postObject.get(slug=slug)
        serializer = PostSerializer(post).data
        client_ip = get_client_ip(request)
        if not PostView.objects.filter(post=post, ip_address=client_ip).exists():
            return Response(serializer)
        PostView.objects.create(post=post, ip_address=client_ip)
        return Response(serializer)

class PostHeadingsView(ListAPIView):
    serializer_class = HeadingSerializer

    def get_queryset(self):
        post_slug = self.kwargs.get('slug')
        return Heading.objects.filter(post__slug=post_slug)