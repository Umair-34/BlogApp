from django.urls import path
from .views import HomeView, DetailView, UpvoteView, CategoryView, TagView, AddSubscriberView, SearchView, ContactUsView

app_name = "core"

urlpatterns = [
    path('', HomeView, name='HomeView'),
    path('blog/<slug:slug>/', DetailView, name='DetailView'),
    path('upvote/<slug:slug>/', UpvoteView, name='UpvoteView'),
    path('category/<slug:slug>/', CategoryView, name='CategoryView'),
    path('tags/<slug:slug>/', TagView, name='TagView'),
    path('subscribe/', AddSubscriberView, name='AddSubscriberView'),
    path('search/', SearchView, name='SearchView'),
    path('contact-us/', ContactUsView, name='ContactUsView'),


]
