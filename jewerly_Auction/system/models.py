from django.db import models

class ValuationRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Chờ xử lý'),
        ('in_progress', 'Đang định giá'),
        ('completed', 'Đã hoàn thành'),
    ]
    
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    origin = models.CharField(max_length=100)
    shape = models.CharField(max_length=100)
    measurements = models.CharField(max_length=100)
    carat_weight = models.DecimalField(max_digits=5, decimal_places=2)
    color = models.CharField(max_length=50)
    clarity = models.CharField(max_length=50)
    cut = models.CharField(max_length=50)
    proportions = models.CharField(max_length=100)
    polish = models.CharField(max_length=50)
    symmetry = models.CharField(max_length=50)
    fluorescence = models.CharField(max_length=50)
    grade = models.CharField(max_length=20)
    date = models.DateField(null=True, blank=True)
    price_range = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.carat_weight} Carat"