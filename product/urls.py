from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

# router = DefaultRouter()
# router.register('products', views.ProductViewSet)
                # .../posts/  -> GET(list), POST(create)
                # .../posts/<id>/  -> GET(retrieve), PUT/PATCH(update),
#                                               DELETE(destroy)

urlpatterns = [
    # path('', include(router.urls)),
    path('comments/', views.CommentCreateView.as_view()),
    path('likes/', views.LikeCreateView.as_view()),
    path('favorite-products/', views.FavoriteCreateView.as_view()),
]
