from django.urls import path
from .views import (
    OrderListCreateView, OrderDetailView, ConfirmOrderView, AssignDriverView
)
from .views import (
    BidCreateView, BidDetailView, AcceptBidView
)
from .views import (
    DriverListView, DriverOrdersView
)
from .views import (
    ProfitView, DispatcherStatsView, CompanyPerformanceView
)

urlpatterns = [
    # Orders
    path("orders/", OrderListCreateView.as_view(), name="order-list-create"),
    path("orders/<int:id>/", OrderDetailView.as_view(), name="order-detail"),
    path("orders/<int:id>/confirm/", ConfirmOrderView.as_view(), name="order-confirm"),
    path("orders/<int:id>/assign-driver/", AssignDriverView.as_view(), name="assign-driver"),

    # Bidding
    path("bids/", BidCreateView.as_view(), name="bid-create"),
    path("bids/<int:id>/", BidDetailView.as_view(), name="bid-detail"),
    path("bids/<int:id>/accept/", AcceptBidView.as_view(), name="accept-bid"),

    # Driver Management
    path("drivers/", DriverListView.as_view(), name="driver-list"),
    path("drivers/<int:id>/orders/", DriverOrdersView.as_view(), name="driver-orders"),

    # Admin Dashboard
    path("admin/profit/", ProfitView.as_view(), name="profit"),
    path("admin/dispatcher-stats/", DispatcherStatsView.as_view(), name="dispatcher-stats"),
    path("admin/company-performance/", CompanyPerformanceView.as_view(), name="company-performance"),
]
