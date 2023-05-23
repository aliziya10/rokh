from django.db.models import Value, F, CharField
from django.db.models.functions import Concat
from django.shortcuts import render, get_object_or_404
from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.utils import timezone
from rest_framework.response import Response
from .serializers import *
from .models import Post,ImagePost
from rest_framework import viewsets







class PostViewSet(viewsets.ModelViewSet):
    queryset = ImagePost.objects.all()
    serializer_class = ImagesSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        # Assuming the `ImagePost` model has a field named `image` that stores the image
        # You can adjust this logic based on your actual model structure

        # Delete the image file from storage (assuming you are using a FileField or ImageField)
        instance.image.delete()

        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)