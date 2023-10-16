from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime, timedelta

class User(AbstractUser):
    pass

class AuctionListing(models.Model):
    auctioneer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="auctioneer")
    auction_id = models.AutoField(primary_key=True)
    item_name = models.CharField(max_length=32)
    item_desc = models.TextField()
    item_image = models.ImageField(upload_to="auction_images/")
    date_created = models.DateField(auto_now_add=True)
    date_ends = models.DateField(default=(datetime.now() + timedelta(days=7)))
    category = models.CharField(max_length=32)
    bid = models.FloatField()
    watchlist = models.ManyToManyField(User, blank=True, related_name="watchlist_user")
    status = models.BooleanField(default=True)


class AuctionBid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_bid")
    auction = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="auction_num")
    bid = models.FloatField()

class AuctionComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    auction = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="id_num")
    comment = models.TextField()