from django.shortcuts import render
from .models import BlogPost, Comment, Categories
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


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
