from django.db import models


class Agent(models.Model):

    Profile_picture=models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    username = models.CharField(max_length=100)
    password = models.TextField()
    Phone= models.CharField(max_length=15, unique=True)
    total_sales = models.DecimalField(max_digits=10, decimal_places=2)
    Total_commission = models.DecimalField(max_digits=10, decimal_places=2)
    Commission_rate = models.DecimalField(max_digits=5, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username
    

class Leads(models.Model):
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE)
    lead_name = models.CharField(max_length=100)
    lead_email = models.EmailField()
    lead_phone = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.lead_name