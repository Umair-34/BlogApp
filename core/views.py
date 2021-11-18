from django.shortcuts import render, redirect, get_object_or_404
from .models import BlogPost, Comment, Categories
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse


def HomeView(request):
    query_set = BlogPost.objects.all().order_by('-post_date')
    paginator = Paginator(query_set, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    context = {
        'count': paginator.count,
        'page': page,
    }
    return render(request, 'core/home.html', context)


def DetailView(request, slug):
    query_set = BlogPost.objects.get(slug=slug)
    related_qs = BlogPost.objects.filter(tags__in=query_set.tags.all()).exclude(slug=slug)[:3]
    comments = query_set.comments.all()
    print("---rs--->", comments)
    if request.method == 'POST':
        message = request.POST.get('message')
        email = request.POST.get('email')
        if request.user.is_authenticated:
            obj = Comment.objects.create(post=query_set, sender=request.user, message=message)
            print(obj.sender, "--1--")
            return JsonResponse(
                {'commenter': obj.sender.first_name + " " + obj.sender.first_name, 'created_at': obj.created_at,
                 'msg': obj.message})
        else:
            obj = Comment.objects.create(post=query_set, sender_email=email, message=message)
            print(obj, "--2--")
            return JsonResponse({'commenter': "Unknown", 'created_at': obj.created_at, 'msg': obj.message})
    context = {
        'object': query_set,
        'related_posts': related_qs,
        'comments': comments,
    }
    return render(request, 'core/detail.html', context)


# def PostComment(request, slug):
#     if request.method == 'POST':
#         message = request.POST.get('message')
#         email = request.POST.get('email')
#         if request.user.is_authenticated:
#             obj = Comment.objects.create(sender=request.user, message=message)
#         else:
#             obj = Comment.objects.create(sender_email=email, message=message)
#
#         query_set = BlogPost.objects.get(slug=slug)
#         query_set.comments.add(obj)
#         query_set.save()
#         return redirect('core:DetailView', slug=slug)
#

def UpvoteView(request, slug):
    upvote_obj = get_object_or_404(BlogPost, slug=request.POST.get('upvote'))
    upvote_obj.upvote.add(request.user)
    upvote_obj.save()
    return HttpResponseRedirect(reverse('core:DetailView', args=[slug]))
