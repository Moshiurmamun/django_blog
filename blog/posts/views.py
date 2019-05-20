from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, HttpResponseRedirect, Http404
from .forms import PostForm
from .models import Post, Category
from django.utils import timezone
from urllib.parse import quote_plus # for social sharing
from django.db.models import Q



# Create your views here.

def post_create(request):


    form = PostForm(request.POST or None, request.FILES or None) # Here for this None required fields are not visible
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        return redirect('post:list')
    context = { 'form': form }
    return render(request, 'posts/post_form.html', context)



def category(request, name):
    today = timezone.now().date() # it used for showing future
    posts = Post.objects.active().order_by('-views')[:5] #for popular posts
    cat = get_object_or_404(Category, name=name)
    post=Post.objects.active().filter(category=cat.id)
    category_list = Category.objects.all()
    if request.user.is_staff or request.user.is_superuser:
        post=Post.objects.filter(category=cat.id)

    query = request.GET.get("q") # for Search posts
    if query:
        post = post.filter(
                Q(title__icontains=query)|
                Q(content__icontains=query)|
                Q(user__first_name__icontains=query)|
                Q(user__last_name__icontains=query)
                ).distinct()

    paginator = Paginator(post, 5) # Show 5 posts per page
    page = request.GET.get('page')
    try:
            queryset = paginator.page(page)
    except PageNotAnInteger:
            queryset = paginator.page(1)
    except EmptyPage:
            queryset = paginator.page(paginator.num_pages)

    context = {
        "cat": cat,
        'today': today,
        'mosts': posts,
        'categories': category_list,
        'object_list': queryset,
    }
    return render(request, 'category/category.html', context)







def post_detail(request, slug=None):
    instance = get_object_or_404(Post, slug=slug)
    posts = Post.objects.active().order_by('-views')[:5]
    category_list = Category.objects.all()
    if instance.draft or instance.publish > timezone.now().date():
        if not request.user.is_staff:
            raise Http404
    share_string = quote_plus(instance.content) # for share content in social sites
    instance.views += 1
    instance.save()

    context = {
        'title': instance.title,
        'instance': instance,
        'share_string': share_string,
        'categories': category_list,
        'mosts': posts,
    }
    return render(request, 'posts/post_detail.html', context)




def post_list(request):
    today = timezone.now().date() # it used for showing future
    posts = Post.objects.active().order_by('-views')[:5] #for popular posts
    queryset_list = Post.objects.active()
    category_list = Category.objects.all()
    if request.user.is_staff or request.user.is_superuser:
        queryset_list = Post.objects.all()

    query = request.GET.get("q") # for Search posts
    if query:
        queryset_list = queryset_list.filter(
                Q(title__icontains=query)|
                Q(content__icontains=query)|
                Q(user__first_name__icontains=query)|
                Q(user__last_name__icontains=query)
                ).distinct()
    paginator = Paginator(queryset_list, 5) # Show 5 posts per page
    page = request.GET.get('page')
    try:
            queryset = paginator.page(page)
    except PageNotAnInteger:
            queryset = paginator.page(1)
    except EmptyPage:
            queryset = paginator.page(paginator.num_pages)

    context = { 'mosts': posts,'object_list': queryset,'categories': category_list ,'title': 'List', 'today': today }

    return render(request, 'posts/post_list.html', context)




def post_update(request, slug=None):
    if not request.user.is_staff:
        raise Http404
    instance = get_object_or_404(Post, slug=slug)
    form = PostForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return redirect('home')
    context = {

		'instance': instance,
		'form': form,
        }
    return render(request, 'posts/post_form.html', context)





def post_delete(request, slug=None):
    if not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Post, slug=slug)
    instance.delete()
    return redirect('home')
