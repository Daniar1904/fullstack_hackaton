from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response

from order.serializers import OrderSerializer


# Create your views here.
class CreateOrderView(ListCreateAPIView):
    serializer_class = OrderSerializer

    def get(self, request, *args, **kwargs):
        user = request.user
        order = user.orders.all()
        serializer = OrderSerializer(order, many=True)
        return Response(serializer.data, status=200)
