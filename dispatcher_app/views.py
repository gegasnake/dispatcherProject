from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

from .models import Order, Company
from .serializers import OrderSerializer
from .models import Bid
from .serializers import BidSerializer
from .models import Driver, Truck
from .serializers import DriverSerializer, TruckSerializer
from django.db.models import Sum


# -------- ORDERS --------
class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]


class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]


class ConfirmOrderView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, id):
        order = get_object_or_404(Order, id=id)
        order.status = 'confirmed'
        order.save()
        return Response({'message': 'Order confirmed successfully'})


class AssignDriverView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, id):
        order = get_object_or_404(Order, id=id)
        driver_id = request.data.get('driver_id')
        driver = get_object_or_404(Driver, id=driver_id)

        order.driver = driver
        order.status = 'assigned'
        order.save()
        return Response({'message': f'Driver {driver.user.email} assigned to order {order.id}'})


# -------- BIDS --------
class BidCreateView(generics.CreateAPIView):
    queryset = Bid.objects.all()
    serializer_class = BidSerializer
    permission_classes = [permissions.IsAuthenticated]


class BidDetailView(generics.RetrieveAPIView):
    queryset = Bid.objects.all()
    serializer_class = BidSerializer
    permission_classes = [permissions.IsAuthenticated]


class AcceptBidView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, id):
        bid = get_object_or_404(Bid, id=id)
        bid.status = 'accepted'
        bid.save()
        return Response({'message': 'Bid accepted successfully'})


# -------- DRIVER MANAGEMENT --------
class DriverListView(generics.ListCreateAPIView):
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer
    permission_classes = [permissions.IsAuthenticated]


class DriverOrdersView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        driver_id = self.kwargs['id']
        return Order.objects.filter(driver_id=driver_id)


# -------- ADMIN DASHBOARD --------
class ProfitView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        total_profit = Order.objects.filter(status='completed').aggregate(Sum('price'))['price__sum']
        return Response({'total_profit': total_profit})


class DispatcherStatsView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        stats = {
            'total_orders': Order.objects.count(),
            'completed_orders': Order.objects.filter(status='completed').count()
        }
        return Response(stats)


class CompanyPerformanceView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        company_stats = {}
        for company in Company.objects.all():
            company_stats[company.name] = Order.objects.filter(company=company).count()
        return Response(company_stats)
