import re

import markdown
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.views.generic import ListView, DetailView
from markdown.extensions.toc import TocExtension, slugify
from pure_pagination import PaginationMixin

from .models import Post, Category, Tag, Profile


# def index(request):
#     post_list = Post.objects.all().order_by('-created_time')
#     return render(request, 'blog/lw-index.html', context={'post_list': post_list})

class IndexView(PaginationMixin, ListView):  # ListView从数据库中获取模型列表数据
    model = Post  # 指定获取的模型
    template_name = 'blog/lw-index.html'  # 指定渲染模板
    context_object_name = 'post_list'  # 指定列表数据保存的变量名

    paginate_by = 10


def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)

    post.increase_views()

    md = markdown.Markdown(extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        'markdown.extensions.toc',
    ])
    post.body = md.convert(post.body)

    m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
    post.toc = m.group(1) if m is not None else ''
    context = {'previous_post': Post.objects.filter(id__lt=pk).first(),
               'next_post': Post.objects.filter(id__gt=pk).last(),
               'post': post}
    # context['previous_post'] = Post.objects.filter(created_time__gt=post.created_time).last()
    # context['next_post'] = Post.objects.filter(created_time__lt=post.created_time).first()
    return render(request, 'blog/lw-article.html', context)


# class PostArticleView(DetailView):
#     # 这些属性的含义和 ListView 是一样的
#     model = Post
#     template_name = 'blog/lw-article.html'
#     context_object_name = 'post'
#
#     def get(self, request, *args, **kwargs):
#         # 覆写 get 方法的目的是因为每当文章被访问一次，就得将文章阅读量 +1
#         # get 方法返回的是一个 HttpResponse 实例
#         # 之所以需要先调用父类的 get 方法，是因为只有当 get 方法被调用后，
#         # 才有 self.object 属性，其值为 Post 模型实例，即被访问的文章 post
#         response = super(PostArticleView, self).get(request, *args, **kwargs)
#
#         # 将文章阅读量 +1
#         # 注意 self.object 的值就是被访问的文章 post
#         self.object.increase_views()
#
#         # 视图必须返回一个 HttpResponse 对象
#         return response
#
#     def get_object(self, queryset=None):
#         # 覆写 get_object 方法的目的是因为需要对 post 的 body 值进行渲染
#         post = super().get_object(queryset=None)
#         md = markdown.Markdown(extensions=[
#             'markdown.extensions.extra',
#             'markdown.extensions.codehilite',
#             # 记得在顶部引入 TocExtension 和 slugify
#             TocExtension(slugify=slugify),
#         ])
#         post.body = md.convert(post.body)
#
#         m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
#         post.toc = m.group(1) if m is not None else ''
#
#         return post


def archive(request, year, month):
    post_list = Post.objects.filter(created_time__year=year,
                                    created_time__month=month
                                    ).order_by('-created_time')
    return render(request, 'blog/lw-index.html', context={'post_list': post_list})


# def category(request, pk):
#     # 记得在开始部分导入 Category 类
#     cate = get_object_or_404(Category, pk=pk)
#     post_list = Post.objects.filter(category=cate).order_by('-created_time')
#     return render(request, 'blog/lw-index.html', context={'post_list': post_list})


class CategoryView(IndexView):

    def get_queryset(self):
        cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        return super(CategoryView, self).get_queryset().filter(category=cate)


def tag(request, pk):
    # 记得在开始部分导入 Tag 类
    t = get_object_or_404(Tag, pk=pk)
    post_list = Post.objects.filter(tags=t).order_by('-created_time')
    return render(request, 'blog/lw-index.html', context={'post_list': post_list})


def search(request):
    q = request.GET.get('q')

    if not q:
        error_msg = "请输入搜索关键词"
        messages.add_message(request, messages.ERROR, error_msg, extra_tags='danger')
        return redirect('blog:index')

    post_list = Post.objects.filter(Q(title__icontains=q) | Q(body__icontains=q))
    return render(request, 'blog/lw-index.html', {'post_list': post_list})


def about(request):
    return render(request, 'blog/lw-about.html')


def timeline(request):
    post_list = Post.objects.all().order_by('-created_time')
    return render(request, 'blog/lw-timeline.html', context={'post_list': post_list})


def contact(request):
    return render(request, 'blog/lw-contact.html')