from django.db import models
from django.contrib.auth import get_user_model
CustomerUser = get_user_model()


class Company(models.Model):
    name = models.CharField(max_length=255, unique=True)
    owner = models.ForeignKey(CustomerUser, on_delete=models.CASCADE, related_name="owned_companies")
    # contact_email = models.EmailField(unique=True)
    # phone_number = models.CharField(max_length=20, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    trucks = models.ManyToManyField("Truck", related_name="associated_companies")

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("assigned", "Assigned"),
        ("completed", "Completed"),
        ("canceled", "Canceled"),
    ]
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="orders")
    driver = models.ForeignKey("Driver", on_delete=models.CASCADE, related_name="orders", null=True, blank=True)
    owner_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    load_type = models.CharField(max_length=20)
    dimensions = models.TextField(blank=True, null=True)
    distance = models.FloatField(help_text="Distance in miles", null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} by {self.user.email}"


class Bid(models.Model):
    delivery_description = models.CharField(max_length=1000)
    estimates = models.IntegerField()
    out = models.IntegerField()
    weight = models.CharField(max_length=200)
    car_type = models.CharField(max_length=100)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="bids")
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="bids")
    created_at = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return f"Bid {self.id} by {self.company.name} for Order {self.order.id}"


class Driver(models.Model):
    user = models.OneToOneField(CustomerUser, on_delete=models.CASCADE, related_name="driver_profile")
    phone = models.CharField(max_length=20)

    def __str__(self):
        return self.user.email


class VirtualLocation(models.Model):
    type = models.CharField(max_length=100)
    address = models.TextField()
    zip_code = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.type} - {self.address}"


class Truck(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('maintenance', 'Maintenance'),
        ('inactive', 'Inactive'),
        ('no_status', 'No Status Chosen'),
    ]

    driver = models.OneToOneField(Driver, on_delete=models.CASCADE, related_name="truck")
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="owned_trucks")
    capacity = models.IntegerField()
    car_type = models.CharField(max_length=50)
    equipped_with = models.CharField(max_length=100, blank=True, null=True)
    virtual_location = models.ForeignKey(VirtualLocation, on_delete=models.SET_NULL, null=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='no_status')
    preferred_radius = models.IntegerField(blank=True, null=True)
    telegram_held = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.company} - {self.car_type}"



