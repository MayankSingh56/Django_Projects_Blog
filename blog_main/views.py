
from django.shortcuts import render
from blogs.models import Blog, Category


def home(request):
    categories = Category.objects.all()
    featured_blog = Blog.objects.filter(status=1, is_featured=True).order_by('-created_at').first()
    blogs = Blog.objects.filter(status=1).order_by('-created_at')

    context = {
        'categories': categories,
        'featured_blog': featured_blog,
        'blogs': blogs,
    }
    return render(request, 'home.html', context)
