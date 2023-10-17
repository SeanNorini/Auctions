from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from django import forms
from datetime import datetime
from .models import *


def index(request):
    auctions = AuctionListing.objects.all()
    return render(request, "auctions/index.html", {"auctions": auctions})


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
    
def listing(request, id):
    comments = AuctionComment.objects.filter(auction=id)
    auction = AuctionListing.objects.filter(pk=id).first()
    bid = AuctionBid.objects.filter(auction=id).order_by("-bid")     
    if len(bid) > 0:
        bid = bid[0]
    if auction is not None:
        watchlist = auction.watchlist.all()
        return render(request, "auctions/listing.html", {"auction": auction, "watchlist": watchlist, "comments": comments, "bid": bid})
    else:
        return render(request, "auctions/listing.html")

def update_watchlist(request, id):
    auction = AuctionListing.objects.filter(pk=id).first()
    if request.method == "POST":
        if request.POST["watchlist"] == "add":
            auction.watchlist.add(request.user)
        else:
            auction.watchlist.remove(request.user)
        return HttpResponseRedirect(reverse("listing", args=(id, )))
    return render(request, "auctions/index.html") 

def bid(request, id):
    if request.method == "POST":
        auction = AuctionListing.objects.filter(pk=id).first()
        if float(request.POST["bid"]) > auction.bid:
            auction.bid = request.POST["bid"]
            auction.save()
            new_bid = AuctionBid()
            new_bid.username  = request.user
            new_bid.auction = AuctionListing.objects.get(auction_id=id)
            new_bid.bid = request.POST["bid"]
            new_bid.save()

            return HttpResponseRedirect(reverse("listing", args=(id, )))
        else:
            return HttpResponseRedirect(reverse("listing", args=(id, )))
    return render(request, "auctions/index.html") 
    

def watchlist(request):
    auctions = request.user.watchlist_user.all()
    return render(request, "auctions/watchlist.html", {"auctions":auctions})


def category(request, category_name):
    if request.method == "POST":
        category_name = request.POST['category']
    auctions = list(AuctionListing.objects.filter(category=category_name))
    if len(auctions) > 0:
        return render(request, "auctions/category.html", {"auctions": auctions})
    else:
        return render(request, "auctions/category.html")
    
def add_listing(request):
    if request.method == "POST":
        form = CreateAuction(request.POST, request.FILES)
        if form.is_valid():
            auction = AuctionListing()
            auction.username  = request.user
            auction.item_name = form.cleaned_data['item_name']
            auction.item_desc = form.cleaned_data['item_desc']
            auction.item_image = form.cleaned_data['item_image']
            auction.date_ends = form.cleaned_data['date_ends']
            auction.category = form.cleaned_data['category']
            auction.bid = form.cleaned_data['bid']
            auction.save()
            return render(request, "auctions/add_listing.html", {"message": "Auction Created.", "form": CreateAuction()})
        else:
            return render(request, "auctions/add_listing.html", {"form": CreateAuction()})    
    else:
        return render(request, "auctions/add_listing.html", {"form": CreateAuction()})  

class CreateAuction(forms.Form):
    item_name = forms.CharField(label="item_name")
    item_desc = forms.CharField(widget=forms.Textarea(attrs={'rows': 4, 'cols': 50, 'label':'item_desc'}))
    item_image = forms.ImageField(label="item_image")
    date_ends = forms.DateField(label="date_ends")
    category = forms.CharField(label="category")
    bid = forms.FloatField(label="bid")

def add_comment(request, id):
    if request.method == "POST":
        new_comment = AuctionComment()
        new_comment.username  = request.user
        new_comment.auction = AuctionListing.objects.get(auction_id=id)
        new_comment.comment = request.POST["comment"]
        new_comment.save()
    return HttpResponseRedirect(reverse("listing", args=(id, )))

def close_auction(request, id):
    if request.method == 'POST':
        auction = AuctionListing.objects.get(auction_id=id)
        auction.status = False
        auction.save()
    return HttpResponseRedirect(reverse("listing", args=(id, )))