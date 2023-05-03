from django.db.models import Value, F, CharField
from django.db.models.functions import Concat
from django.shortcuts import render, get_object_or_404
from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.utils import timezone
from rest_framework.response import Response
from .serializers import PostSerializer
from .models import Post




@api_view(['POST'])
@permission_classes([AllowAny])
def create_post(request):
    serializer = PostSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(author=request.user, dateOfPublish=timezone.now())
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)




@api_view(['POST', 'PUT', 'DELETE',"GET"])
@permission_classes([IsAuthenticated])
def post_detail(request, pk=None):
    if request.method == 'POST':
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user, dateOfPublish=timezone.now())
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    post = get_object_or_404(Post, pk=pk)

    if request.method == 'PUT':
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    elif request.method=="GET":
        base_url = "https://server.hanousa.ir/images/"
        # poli="id","title","sub_title","image_url","dateOfPublish","author"

        try:

            posts = Post.objects.values().get(id=pk)

            return Response(posts, status=status.HTTP_200_OK)

        except (ValueError, Post.DoesNotExist):
            return Response({}, status=status.HTTP_404_NOT_FOUND)

    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


