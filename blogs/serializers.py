from .models import Blog
from rest_framework import serializers

class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = '__all__'
class BlogListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ("id", "title", "mini_content", "mobile_image")