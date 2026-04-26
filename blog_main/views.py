
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from blogs.forms import BlogForm, LoginForm, RegisterForm
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
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful. You are now logged in.')
            return redirect('home')
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            messages.success(request, 'Welcome back. You are logged in now.')
            return redirect('home')
    else:
        form = LoginForm(request)

    return render(request, 'login.html', {'form': form})


@login_required
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        messages.success(request, 'You have been logged out.')
    return redirect('home')


@login_required
def create_blog(request):
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user
            blog.save()
            messages.success(request, 'Your blog has been created successfully.')
            return redirect('home')
    else:
        form = BlogForm()

    return render(request, 'create_blog.html', {'form': form})
