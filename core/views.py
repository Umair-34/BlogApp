import datetime
from random import randint

from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect, get_object_or_404
from .models import BlogPost, Comment, Categories, Subscriber, Contact
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from taggit.models import Tag


def PopularPosts():
    week_ago = datetime.date.today() - datetime.timedelta(days=7)
    trends = BlogPost.objects.filter(post_date__gte=week_ago).order_by('-id')[:6]
    if len(trends) < 6:
        month_ago = datetime.date.today() - datetime.timedelta(days=30)
        trends = BlogPost.objects.filter(post_date__gte=month_ago).order_by('-id')[:6]
    return trends


def HomeView(request):
    query_set = BlogPost.objects.all().order_by('-id')
    trends = PopularPosts()
    categories_qs = Categories.objects.all()
    paginator = Paginator(query_set, 4)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    context = {
        'count': paginator.count,
        'page': page,
        'category': categories_qs,
        'tags': Tag.objects.all(),
        'trends': trends,
    }
    return render(request, 'core/home.html', context)


def DetailView(request, slug):
    query_set = BlogPost.objects.get(slug=slug)
    related_qs = BlogPost.objects.filter(tags__in=query_set.tags.all()).exclude(slug=slug)[:3]
    trends = PopularPosts()
    comments = query_set.comments.all().order_by('-id')

    if request.method == 'POST':
        message = request.POST.get('message')
        email = request.POST.get('email')
        if message is not None:
            print("check")
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
        'trends': trends,
    }
    return render(request, 'core/detail.html', context)


def UpvoteView(request, slug):
    query_set = BlogPost.objects.get(slug=slug)
    print(query_set, "qs--->1")
    query_set.upvote.add(request.user)
    query_set.save()
    print(query_set, "qs--->1")

    return redirect('core:DetailView', slug=slug)


def CategoryView(request, slug):
    query_set = BlogPost.objects.select_related('category').filter(category__category_name=slug)
    paginator = Paginator(query_set, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    trends = PopularPosts()

    context = {
        'count': paginator.count,
        'page': page,
        'slug': slug,
        'trends': trends,
    }
    return render(request, 'core/category_and_tags.html', context)


def TagView(request, slug):
    query_set = BlogPost.objects.filter(tags__slug=slug)
    print(query_set, "tags--->")
    paginator = Paginator(query_set, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    trends = PopularPosts()

    context = {
        'count': paginator.count,
        'page': page,
        'slug': slug,
        'trends': trends,
    }
    return render(request, 'core/category_and_tags.html', context)


def AddSubscriberView(request):
    if request.method == "POST":
        email = request.POST.get('email')
        if Subscriber.objects.filter(email=email).exists():
            return JsonResponse({'added': "False", })
        else:
            Subscriber.objects.create(email=email)
            return JsonResponse({'added': "True", })


def SearchView(request):
    trends = PopularPosts()
    if request.method == 'POST':
        query = request.POST.get('search_form')
    if len(query) > 80:
        all_posts = BlogPost.objects.none()
    elif len(query) <= 3:
        all_posts = BlogPost.objects.none()
    else:
        all_posts_title = BlogPost.objects.filter(title__icontains=query)
        all_posts_blog = BlogPost.objects.filter(blog__icontains=query)
        all_posts = all_posts_blog.union(all_posts_title)
    context = {
        'allPosts': all_posts,
        'query': query,
        'trends': trends,
    }
    return render(request, 'core/search.html', context)


def ContactUsView(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('msg')
        Contact.objects.create(name=name, email=email, message=message)
        messages.info(request,
                      'We appreciate you for contacting us. One of our colleagues will get back in touch with you soon!Have a great day!')
    trends = PopularPosts()
    context = {
        'trends': trends,
    }
    return render(request, 'core/contact_us.html', context)
