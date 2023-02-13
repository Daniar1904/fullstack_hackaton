from django.shortcuts import render
from rest_framework import permissions
from rest_framework.decorators import action

from . import serializers
from rest_framework.viewsets import ModelViewSet

from product.models import Product
from .permissions import IsAuthor


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.ProductListSerializer
        return serializers.ProductSerializer

    def get_permissions(self):
        if self.action in ('update', 'partial_update', 'destroy'):
            return [permissions.IsAuthenticated(), IsAuthor]
        return [permissions.IsAuthenticatedOrReadOnly()]



