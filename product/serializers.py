from django.db.models import Avg
from rest_framework import serializers
from .models import Product, Comment, Like, Favorites


from rating.serializers import ReviewSerializer
from .models import Product, Comment, Like, Favorites, ProductImages



class ProductListSerializer(serializers.ModelSerializer):
    owner_email = serializers.ReadOnlyField(source='owner.email')

    class Meta:
        model = Product
        fields = ('category', 'owner_email', 'title', 'price', 'image', 'stock', 'description')

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        print(instance, '!!!!!!')
        repr['rating'] = instance.reviews.aggregate(Avg('rating'))['rating__avg']
        return repr

        # def to_representation(self, instance):
    #     repr = super().to_representation(instance)
    #     repr['rating'] = instance.reviews.aggregate(Avg('rating'))['rating__avg']
    #     repr['comments_count'] = instance.comments.count()
    #     repr['comments'] = CommentSerializer(instance.comments.all(),
    #                                         many=True).data
    #     repr['images'] = PostImageSerializer(instance.images.all(),
    #                                         many=True).data
    #     repr['likes_count'] = instance.likes.count()
    #     repr['liked_users'] = LikeSerializer(instance=instance.likes.all(),
    #                                         many=True).data
    #     return repr

class ProductDetailSerializer(serializers.ModelSerializer):
    owner_username = serializers.ReadOnlyField(source='owner.username')
    category_name = serializers.ReadOnlyField(source='category.name')

    class Meta:
        model = Product
        fields = '__all__'

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['comments_count'] = instance.comments.count()
        rep['comments'] = CommentSerializer(instance.comments.all(),
                                            many=True).data
        rep['images'] = PostImageSerializer(instance.images.all(),
                                            many=True).data
        rep['likes_count'] = instance.likes.count()
        rep['liked_users'] = LikeSerializer(instance=instance.likes.all(),
                                            many=True).data
        return rep


class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImages
        fields = '__all__'


# class ProductDetailSerializer(serializers.ModelSerializer):
#     owner_username = serializers.ReadOnlyField(source='owner.username')
#     category_name = serializers.ReadOnlyField(source='category.name')
#
#     class Meta:
#         model = Product
#         fields = '__all__'
#
#     def to_representation(self, instance):
#         rep = super().to_representation(instance)
#         rep['comments_count'] = instance.comments.count()
#         rep['comments'] = CommentSerializer(instance.comments.all(),
#                                             many=True).data
#         rep['images'] = PostImageSerializer(instance.images.all(),
#                                             many=True).data
#         rep['likes_count'] = instance.likes.count()
#         rep['liked_users'] = LikeSerializer(instance=instance.likes.all(),
#                                             many=True).data
#         return rep


class ProductDetailSerializer(serializers.ModelSerializer):
    owner_username = serializers.ReadOnlyField(source='owner.username')
    category_name = serializers.ReadOnlyField(source='category.name')

    class Meta:
        model = Product
        fields = '__all__'

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['comments_count'] = instance.comments.count()
        rep['comments'] = CommentSerializer(instance.comments.all(),
                                            many=True).data
        rep['images'] = PostImageSerializer(instance.images.all(),
                                            many=True).data
        rep['likes_count'] = instance.likes.count()
        rep['liked_users'] = LikeSerializer(instance=instance.likes.all(),
                                            many=True).data
        return rep


class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImages
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    owner_email = serializers.ReadOnlyField(source='owner.email')
    owner = serializers.ReadOnlyField(source='owner.id')
    # reviews = ReviewSerializer(many=True)

    class Meta:
        model = Product
        fields = '__all__'

    @staticmethod
    def get_stars(instance):
        stars = {'5': instance.reviews.filter(rating=5).count(), '4': instance.reviews.filter(rating=4).count(),
                 '3': instance.reviews.filter(rating=3).count(), '2': instance.reviews.filter(rating=2).count(),
                 '1': instance.reviews.filter(rating=1).count()}
        return stars

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr['rating'] = instance.reviews.aggregate(Avg('rating'))
        rating = repr['rating']
        rating['ratings_count'] = instance.reviews.count()
        repr['stars'] = self.get_stars(instance)
        return repr


class CommentSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.id')
    owner_username = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Comment
        fields = '__all__'


class LikeSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.id')
    owner_username = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Like
        fields = '__all__'


    def validate(self, attrs):
        request = self.context['request']
        user = request.user
        product = attrs['product']
        if user.liked_products.filter(product=product).exists():
            raise serializers.ValidationError('You already liked this post!')
        return

    # def validate(self, attrs):
    #     request = self.context['request']
    #     user = request.user
    #     product = attrs['product']
    #     if user.liked_products.filter(product=product).exists():
    #         raise serializers.ValidationError('You already liked this post!')
    #     return


class FavoriteProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorites
        fields = ('id', 'product')

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr['product_title'] = instance.product.title
        return repr
