from django.shortcuts import render
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, APIException
from .models import Post, Category, Heading, PostAnalytics, PostView
from .serializers import PostSerializer, PostListSerializer, CategorySerializer, HeadingSerializer
from .utils import get_client_ip
from .tasks import increment_post_view


# Create your views here.
'''class PostListView(ListAPIView):
    queryset = Post.postObject.all()
    serializer_class = PostListSerializer'''

class PostListView(APIView):
    def get(self, request, *args, **kwargs):
        posts = Post.postObject.all()
        serializer = PostListSerializer(posts, many=True).data
        for post in posts:
            increment_post_view.delay(post.id)
        return Response(serializer)

    
'''class PostDetailView(RetrieveAPIView):
        queryset = Post.postObject.all()
        serializer_class = PostSerializer
        lookup_field = 'slug'''

class PostDetailView(APIView):
    def get(self, request, slug):
        try:
            post = Post.postObject.get(slug=slug)
        except Post.DoesNotExist:
            raise NotFound("An error occurred while retrieving the post")
        except Exception as e:
            raise APIException("An unexpected error occurred: " + str(e))
        
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
    
class IncrementPostClicksView(APIView):
    def post(self, request):
        """Increment the click count for a specific post identified by its slug."""
        data = request.data
        try:
            post = Post.postObject.get(slug=data.get('slug'))
            analytics, created = PostAnalytics.objects.get_or_create(post=post)
            analytics.increment_clicks()
            analytics.save()
            return Response({"message": "Click recorded"})
        except Post.DoesNotExist:
            raise NotFound("Post not found")
        except Exception as e:
            raise APIException("An unexpected error occurred: " + str(e))