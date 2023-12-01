from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("createlisting", views.createlisting, name="createlisting"),
    path("<int:pk>", views.item, name="item"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("removewatchlist", views.removewatchlist, name="removewatchlist"),
    path("closeauction", views.closeauction, name="closeauction"),
    #not done this function yet:  path("payment", views.payment, name="payment"), 
    path("comment", views.comment, name="comment"),
    path("category", views.category, name="category"),
    path("category/<int:pk>", views.smallcategory, name="smallcategory"),
]
