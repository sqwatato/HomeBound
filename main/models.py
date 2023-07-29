from django.db import models

# Create your models here.

class Shelter(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    lat = models.DecimalField(max_digits=19, decimal_places=16, null=True, blank=True)
    lon = models.DecimalField(max_digits=19, decimal_places=16, null=True, blank=True)

    def __str__(self):
        return self.name

class Opportunity(models.Model):
    ADOPTION = 'A' 
    FOSTERING = 'F' 
    TYPE_CHOICES = [ 
        (ADOPTION, 'Adoption'),
        (FOSTERING, 'Fostering'),
    ]
    type = models.CharField(max_length=1, choices=TYPE_CHOICES)
    shelter = models.ForeignKey(Shelter, on_delete=models.CASCADE, related_name='opportunities') 
    name = models.CharField(max_length=50) 
    species = models.CharField(max_length=50) 
    breed = models.CharField(max_length=50)
    age = models.IntegerField()
    gender = models.CharField(max_length=1, choices=[('M', 'Male'), ('F', 'Female')]) 
    description = models.TextField(blank=True) 
    image = models.ImageField(upload_to='pets') 
    urgent = models.BooleanField(default=False) 
    available = models.BooleanField(default=True) 

    def __str__(self):
        return f'{self.type}: {self.name}'
