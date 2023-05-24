from django.contrib.auth.models import User
from Posts.models  import *
from rest_framework import serializers

class TagSerializers(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id','title')

class PostSerializers(serializers.ModelSerializer):
    tags = TagSerializers(many=True)
    class Meta:
        model = Post
        fields = ("id","title","text","sub_title","image_url","persian_date","author",'tags')