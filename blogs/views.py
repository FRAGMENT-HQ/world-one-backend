from django.shortcuts import render
from .serializers import BlogSerializer,BlogListSerializer
from rest_framework.generics import ListAPIView,RetrieveAPIView
from .models import Blog

class BlogList(ListAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogListSerializer

class BlogDetail(RetrieveAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'blog_id'


# Create your views here.
