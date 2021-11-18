from django.urls import path
from .views import HomeView, DetailView, UpvoteView

app_name = "core"

urlpatterns = [
    path('', HomeView, name='HomeView'),
    path('blog/<slug:slug>/', DetailView, name='DetailView'),
    # path('post-comment/<slug:slug>/', PostComment, name='PostComment'),
    path('upvote/<slug:slug>/', UpvoteView, name='UpvoteView'),

]
