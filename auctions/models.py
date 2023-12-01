from django.contrib.auth.models import AbstractUser, User
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class Listing(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    startBid = models.IntegerField()
    imageURL = models.URLField(max_length=200, blank=True, null=True)  
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')
    is_sold = models.BooleanField(default=False)
    winner = models.ForeignKey(User, on_delete=models.CASCADE,   blank=True, null=True, related_name='wins')
    def __str__(self):
        return self.title

class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='bids')
    bid = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bids')
    def __str__(self):
        return f"{self.bid} bid on {self.listing}"
    
class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='watchlist')
    def __str__(self):
        return f'watchlist on item : {self.listing}'
    
class Comment(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='comment')
    content = models.CharField(max_length=500)
    def __str__(self):
        return f'comment on item: {self.listing}'