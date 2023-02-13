from django.shortcuts import render
from rest_framework import permissions, response, generics
from rest_framework.decorators import action

from rating.serializers import ReviewActionSerializer
from . import serializers
from rest_framework.viewsets import ModelViewSet

from product.models import Product, Comment, Like
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
        return [permissions.IsAuthenticatedOrReadOnly]

    @action(['GET', 'POST'], detail=True)
    def reviews(self, request, pk):
        product = self.get_object()
        if request.method == 'GET':
            reviews = product.reviews.all()
            serializer = ReviewActionSerializer(reviews, many=True).data
            return response.Response(serializer, status=200)
        else:
            if product.reviews.filter(owner=request.user).exists():
                return response.Response('You already reviewed this product!', status=400)
            data = request.data
            serializer = ReviewActionSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save(owner=request.user, product=product)
            return response.Response(serializer.data, status=201)

    @action(['DELETE'], detail=True)
    def review_delete(self, request, pk):
        product = self.get_object()
        user = request.user
        if not product.reviews.filter(owner=user).exists():
            return response.Response('You didn\'t reviewed this product!', status=400)
        review = product.reviews.get(owner=user)
        review.delete()
        return response.Response('Successfully deleted!', status=204)


class CommentCreateView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LikeCreateView(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.LikeSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LikeDeleteView(generics.DestroyAPIView):
    queryset = Like.objects.all()
    permission_classes = (permissions.IsAuthenticated, IsAuthor)


class FavoriteCreateView(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.FavoriteProductSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)