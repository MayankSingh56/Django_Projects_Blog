
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from blogs.forms import RegisterForm
from blogs.models import Blog, Category


def home(request):
    categories = Category.objects.all()
    featured_blog = Blog.objects.filter(status=1, is_featured=True).order_by('-created_at').first()
    blogs = Blog.objects.filter(status=1).order_by('-created_at')
    search_query = request.GET.get('q', '').strip()

    if search_query:
        blogs = blogs.filter(
            Q(title__icontains=search_query)
            | Q(short_description__icontains=search_query)
            | Q(blog_body__icontains=search_query)
            | Q(category__category_name__icontains=search_query)
            | Q(author__username__icontains=search_query)
        )
        featured_blog = None

    context = {
        'categories': categories,
        'featured_blog': featured_blog,
        'blogs': blogs,
        'search_query': search_query,
        'page_title': f'Search results for "{search_query}"' if search_query else 'Latest Articles',
    }
    return render(request, 'home.html', context)


def category_posts(request, category_id):
    categories = Category.objects.all()
    category = get_object_or_404(Category, id=category_id)
    search_query = request.GET.get('q', '').strip()
    featured_blog = Blog.objects.filter(
        status=1,
        is_featured=True,
        category=category,
    ).order_by('-created_at').first()
    blogs = Blog.objects.filter(status=1, category=category).order_by('-created_at')

    if search_query:
        blogs = blogs.filter(
            Q(title__icontains=search_query)
            | Q(short_description__icontains=search_query)
            | Q(blog_body__icontains=search_query)
            | Q(author__username__icontains=search_query)
        )
        featured_blog = None

    context = {
        'categories': categories,
        'featured_blog': featured_blog,
        'blogs': blogs,
        'active_category': category,
        'search_query': search_query,
        'page_title': (
            f'Search results for "{search_query}" in {category.category_name}'
            if search_query
            else f'{category.category_name} Articles'
        ),
    }
    return render(request, 'home.html', context)


def github(request):
    return render(request, 'github.html')


def linkedin(request):
    return render(request, 'linkedin.html')


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful. You can log in now.')
            return redirect('home')
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})
