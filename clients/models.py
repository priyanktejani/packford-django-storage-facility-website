from django.db import models


# Create your models here.
class Location(models.Model):
    CITY_CHOICES = (
        ('London', 'London'),
        ('Sheffield', 'Sheffield'),
        ('Liverpool', 'Liverpool'),
        ('Bristol', 'Bristol'),
        ('Hertfordshire', 'Hertfordshire'),
        ('Birmingham', 'Birmingham'),
        ('Wales', 'Wales'),
        ('Kent', 'Kent'),
        ('Leicester', 'Leicester'),
        ('Coventry', 'Coventry'),   
    )
    postcode = models.CharField(max_length=8)
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=20, choices=CITY_CHOICES)
    country = models.CharField(max_length=20)
    phone = models.CharField(max_length=10)

    def __str__(self):
        return self.address + ", Postcode:" + self.postcode


class Company(models.Model):
    company_name = models.CharField(max_length=30, unique=True)
    location = models.OneToOneField(Location, on_delete=models.CASCADE, null=True) # remove null

    def __str__(self):
        return self.company_name


class Branch(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    branch_name = models.CharField(max_length=30, unique=True)
    location = models.OneToOneField(Location, on_delete=models.CASCADE, null=True) # remove null

    def __str__(self):
        return self.branch_name