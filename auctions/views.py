from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.db.models import Max



from .models import *
from .forms import *


def index(request):    
    return render(request, "auctions/index.html", {
        'items': Listing.objects.filter(is_sold=False)
    })


def item(request, pk):
    
    item = get_object_or_404(Listing, pk=pk)  
    isOwner = request.user == item.user
    if request.method == "POST":
            newBid = request.POST["newBid"]
            postBid = Bid(listing=item, bid=newBid, user=request.user)
            postBid.save()
    isWinner = request.user == item.winner
    comments = Comment.objects.filter(listing = item)
    bigBid = Bid.objects.filter(listing=item).order_by('bid').last()
    return render(request, "auctions/item.html",{
        'item': item,
        'bid' : bigBid, 
        'isOwner': isOwner,
        'isWinner': isWinner,
        'comments': comments,
    })


def category(request):
    category = Category.objects.all()
    return render(request, "auctions/category.html", {
        'categories': category
    })

def smallcategory(request, pk):
    category = Category.objects.get(pk=pk)
    items = Listing.objects.filter(category=category)
    return render(request, "auctions/smallcategory.html", {
        'category': category,
        'items': items,
    })
    pass



def createlisting(request):
    if request.method == "POST":
        form = NewItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.user = request.user
            item.save()
            return redirect('item', pk=item.id)
    else:
        form = NewItemForm()
    return render(request, "auctions/createlisting.html", {
        'form': NewItemForm()
    })


@login_required
def watchlist(request):
    watchList = Watchlist.objects.filter(user=request.user)
    if request.method == "POST":
        pk = request.POST["item-pk"]
        item = get_object_or_404(Listing, pk=pk)
        exist =  Watchlist.objects.filter(user=request.user, listing=item)   
        if not exist:         
            newWatchlist = Watchlist(user=request.user, listing=item)
            newWatchlist.save()
        return HttpResponseRedirect(reverse("watchlist"))
    
    return render(request, "auctions/watchlist.html", {
        "watchlist": watchList
    })

@login_required
def removewatchlist(request):
    if request.method == "POST":
        for pk in request.POST:
            if request.POST[pk] == 'on':
                item = get_object_or_404(Listing, pk=pk)
                Watchlist.objects.get(user=request.user, listing=item).delete()
    return HttpResponseRedirect(reverse("watchlist"))


@login_required
def closeauction(request):
    if request.method == "POST":
        item = get_object_or_404(Listing, pk=request.POST['item-pk'])
        if item.user == request.user:
            item.is_sold = True
            winner = Bid.objects.filter(listing=item).order_by('bid').last().user
            item.winner = winner
            item.save()
            return HttpResponseRedirect(reverse("index"))
    pass


@login_required
def payment(request):
    pass


@login_required
def comment(request):
    if request.method == "POST":
        item = get_object_or_404(Listing, pk=request.POST['item-pk'])
        newComment = Comment(creator=request.user, listing=item, content=request.POST['comment'])
        newComment.save()
        return HttpResponseRedirect(reverse("item", args=(item.pk,)))


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

