from django.db import models

# Create your models here.
class Customer(models.Model):
    name=models.CharField(max_length=200,null=True)
    phone=models.CharField(max_length=200,null=True)
    email=models.CharField(max_length=200,null=True)
    date_created=models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name=models.CharField(max_length=200,null=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    CATAGORY =(
        ('Indoor','Indoor'),
        ('Out Door','Out Door'),
    )
    name=models.CharField(max_length=200,null=True)
    price=models.FloatField(max_length=200,null=True)
    category=models.CharField(max_length=200,null=True,choices=CATAGORY)
    description=models.CharField(max_length=200,null=True)
    date_created=models.DateTimeField(auto_now_add=True,null=True)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.name

class Order(models.Model):
    customer=models.ForeignKey(Customer,null=True,on_delete=models.SET_NULL)
    product=models.ForeignKey(Product,null=True,on_delete=models.SET_NULL)
    STATUS = (
        ('pending','pending'),
        ('Out for delivery','Out for delivery'),
        ('Delivered','Delivered'),
    )
    date_created=models.DateTimeField(auto_now_add=True,null=True)
    status = models.CharField(max_length=200, null=True,choices=STATUS)
    note = models.CharField(max_length=2000, null=True)
    def __str__(self):
        return self.product.name

