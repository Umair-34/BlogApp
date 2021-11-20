from django.shortcuts import render, redirect, get_object_or_404
from .models import BlogPost, Comment, Categories
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from taggit.models import Tag


def HomeView(request):
    query_set = BlogPost.objects.all().order_by('-post_date')
    categories_qs = Categories.objects.all()
    paginator = Paginator(query_set, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    context = {
        'count': paginator.count,
        'page': page,
        'category': categories_qs,
        'tags': Tag.objects.all()
    }
    return render(request, 'core/home.html', context)


def DetailView(request, slug):
    query_set = BlogPost.objects.get(slug=slug)
    related_qs = BlogPost.objects.filter(tags__in=query_set.tags.all()).exclude(slug=slug)[:3]
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

    context = {
        'count': paginator.count,
        'page': page,
        'slug': slug,
    }
    return render(request, 'core/category_and_tags.html', context)


def TagView(request, slug):
    query_set = BlogPost.objects.filter(tags__slug=slug)
    print(query_set, "tags--->")
    paginator = Paginator(query_set, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    context = {
        'count': paginator.count,
        'page': page,
        'slug': slug,
    }
    return render(request, 'core/category_and_tags.html', context)
