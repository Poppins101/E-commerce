from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    title = models.CharField(max_length=30)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to='product', blank = True, null=True )
    sold = models.BooleanField(default=False)
    date = models.DateField()
    
    def __str__(self):
        return f" {self.title}"

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_comment')
    product = models.ManyToManyField(Product, related_name='comment_product')
    comment = models.TextField()
    def __str__(self):
        return f"{self.user} commented this {self.comment} on {self.product}"

class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_bid')
    product = models.ManyToManyField(Product, related_name='bid_product')
    bid = models.DecimalField(max_digits=10, decimal_places=2)
    def __str__(self):
        return f"{self.user} bidded {self.bid} to {self.product}"

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_watchlist')
    product = models.ManyToManyField(Product, related_name='watchlist_product')
      