from django.db import models
from django.contrib.auth import get_user_model
from django.db import models
from category.models import Category
from ckeditor.fields import RichTextField


User = get_user_model()


class Product(models.Model):
    STATUS_CHOICES = (
        ('in_stock', 'В наличии'),
        ('out_of_stock', 'Нет в наличии')
    )

    owner = models.ForeignKey(User, on_delete=models.RESTRICT, related_name='products')
    title = models.CharField(max_length=150)
    description = RichTextField()
    category = models.ForeignKey(Category, related_name='products', on_delete=models.RESTRICT)
    image = models.ImageField(upload_to='images')
    price = models.DecimalField(max_digits=12, decimal_places=2)
    stock = models.CharField(choices=STATUS_CHOICES, max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    owner = models.ForeignKey('account.CustomUser', related_name='comments',
                                  on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='comments',
                                 on_delete=models.CASCADE)
    body = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.owner} -> {self.product} -> {self.created_at}'


class Like(models.Model):
    owner = models.ForeignKey('account.CustomUser', on_delete=models.CASCADE,
                              related_name='liked_products')
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                             related_name='likes')

    class Meta:
        unique_together = ['owner', 'product']


class Favorites(models.Model):
    owner = models.ForeignKey('account.CustomUser', on_delete=models.CASCADE,
                              related_name='favorites')
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                             related_name='favorites')

    class Meta:
        unique_together = ['owner', 'product']