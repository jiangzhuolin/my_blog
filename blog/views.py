# -*- coding:utf-8 -*-
import logging
import json

from django.shortcuts import render,redirect,HttpResponse
from django.conf import settings
from django.core.paginator import Paginator,InvalidPage,EmptyPage,PageNotAnInteger
from django.db.models import Count
from django.core.urlresolvers import reverse
from django.contrib.auth import logout,login,authenticate
from django.contrib.auth.hashers import make_password


from blog.forms import *
from blog.models import *


# Create your views here.
# Initial a logger handler
logger = logging.getLogger("blog.views")

# 定义一个方法，返回 settings 文件中的内容
def global_setting(request):
    SITE_NAME=settings.SITE_NAME
    SITE_DESC = settings.SITE_DESC
    SITE_URL = settings.SITE_URL
    # 分类数据
    category_list = Category.objects.all()
    # 文章归档数据
    archive_list = Article.objects.distinct_date()
    # 广告数据
    # 标签云数据
    # 友情链接
    # 文章排行榜
    # 评论排行
    # 从Comment模型中取出article并按article分组计数，再按计数的由高到低排序
    comment_count_list = Comment.objects.values('article').annotate(comment_count=Count('article')).order_by('-comment_count')
    article_comment_list = [Article.objects.get(pk=comment['article']) for comment in comment_count_list]
    return locals()
    '''
    return {
         'category_list':category_list
        ,'archive_list':archive_list
        ,'article_comment_list':article_comment_list
        ,'SITE_NAME':settings.SITE_NAME
        ,'SITE_DESC':settings.SITE_DESC
             }
        '''

# 定义index请求的响应方法
def index(request):
    try:

        # 广告数据
        # 获取最新文章对象
        article_list = Article.objects.all()
        '''
        # 创建分页器的对象，每5条数据分一页
        paginator = Paginatorarticle_list,5)
        try:
            # 获取http请求中传递的page参数的值，如果没有page参数，则默认为1
            page = int(request.GET.get('page',1))
            # 将指定页数的文章数据重新赋值给article_list
            article_list = paginator.page(page)
        except (EmptyPage,InvalidPage,PageNotAnInteger):
            # 分页参数异常时，默认显示的数据
            article_list = paginator.page(1)
        '''
        article_list = getPage(request,article_list)
        # 文章归档
        # 1、先要获取到文章中有的年份-月份 示例：2017/03文章归档
        # 联想到去重函数 Article.objects.values('date_publish').distinct()，但此处不适用，因为需要的只要年月，但date_publist是到时分秒
        #   cursor = connection.cursor()
        #    cursor.execute(
        #        "SELECT DISTINCT DATE_FORMAT(date_publish, '%%Y-%%m') as col_date FROM blog_article ORDER BY date_publish")
        #    archive_list = cursor.fetchall()

        archive_list = Article.objects.distinct_date()
    except Exception as e:
        print(e)
        logger.error(e)
    # locals() 函数可以将当前作用域的所有变量封装并传递给模板
    return render(request, 'index.html', locals())

# 文章归档处理
def archive(request):

    try:
        # 先获取客户端提交的信息
        year = request.GET.get('year',None)
        month = request.GET.get('month', None)
        # 查询category，并且返回
        category_list = Category.objects.all()
        # 广告数据
        # 通过filter获取归档文章对象
        article_list = Article.objects.filter(date_publish__icontains=year+'-'+month)

        article_list = getPage(request,article_list)
    except Exception as e:
        logger.error(e)
    return render(request,'archive.html',locals())


# 分页处理
def getPage(request,article_list):
    # 创建分页器的对象，每5条数据分一页
    paginator = Paginator(article_list, 5)
    try:
        # 获取http请求中传递的page参数的值，如果没有page参数，则默认为1
        page = int(request.GET.get('page', 1))
        # 将指定页数的文章数据重新赋值给article_list
        article_list = paginator.page(page)
    except (EmptyPage, InvalidPage, PageNotAnInteger):
        # 分页参数异常时，默认显示的数据
        article_list = paginator.page(1)
    return article_list

# 文章详情页
def article(request):
    # 获取文章 ID
    article_id = request.GET.get('id', None)
    try:
        article = Article.objects.get(pk=article_id)
    except Article.DoesNotExist:
        return  render(request,'failure.html',{'reason':'The Article is not EXIST!'})

    try:
        # 评论表单
        comment_form = CommentForm({'author': request.user.username,
                                    'email': request.user.email,
                                    'url': request.user.url,
                                    'article': id} if request.user.is_authenticated() else{'article': id})

        # 获取评论信息
        #comments_count = Comment.objects.filter(article=article_id).count()
        comments = Comment.objects.filter(article=article_id).order_by('id')
        comment_list = []

        # 使用循环对评论层级进行处理
        for comment in comments:
            print(comment.content)
            for each in comment_list:
                if not hasattr(each,'children_comment'):
                    setattr(each,'children_comment',[])
                if comment.pid == each:
                    each.children_comment.append(comment)
                    break
            if comment.pid is None:
                    comment_list.append(comment)
        print(comment_list)

    except Exception as e:
        logger.error(e)

    return render(request,'article.html',locals())


# 提交评论
def comment_post(request):
    try:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            #获取表单信息
            comment = Comment.objects.create(username=comment_form.cleaned_data["author"],
                                             email=comment_form.cleaned_data["email"],
                                             url=comment_form.cleaned_data["url"],
                                             content=comment_form.cleaned_data["comment"],
                                             article_id=comment_form.cleaned_data["article"],
                                             user=request.user if request.user.is_authenticated() else None)
            comment.save()
        else:
            return render(request, 'failure.html', {'reason': comment_form.errors})
    except Exception as e:
        logger.error(e)
    return redirect(request.META['HTTP_REFERER'])

# 注销
def do_logout(request):
    try:
        logout(request)
    except Exception as e:
        logger.error(e)
    return redirect(request.META['HTTP_REFERER'])

# 注册
def do_reg(request):
    try:
        if request.method == 'POST':
            reg_form = RegForm(request.POST)
            if reg_form.is_valid():
                # 注册
                user = User.objects.create(username=reg_form.cleaned_data["username"],
                                    email=reg_form.cleaned_data["email"],
                                    url=reg_form.cleaned_data["url"],
                                    password=make_password(reg_form.cleaned_data["password"]),)
                user.save()

                # 登录
                user.backend = 'django.contrib.auth.backends.ModelBackend' # 指定默认的登录验证方式
                login(request, user)
                return redirect(request.POST.get('source_url'))
            else:
                return render(request, 'failure.html', {'reason': reg_form.errors})
        else:
            reg_form = RegForm()
    except Exception as e:
        logger.error(e)
    return render(request, 'reg.html', locals())

# 登录
def do_login(request):
    try:
        if request.method == 'POST':
            login_form = LoginForm(request.POST)
            if login_form.is_valid():
                # 登录
                username = login_form.cleaned_data["username"]
                password = login_form.cleaned_data["password"]
                user = authenticate(username=username, password=password)
                if user is not None:
                    user.backend = 'django.contrib.auth.backends.ModelBackend' # 指定默认的登录验证方式
                    login(request, user)
                else:
                    return render(request, 'failure.html', {'reason': '登录验证失败'})
                return redirect(request.POST.get('source_url'))
            else:
                return render(request, 'failure.html', {'reason': login_form.errors})
        else:
            login_form = LoginForm()
    except Exception as e:
        logger.error(e)
    return render(request, 'login.html', locals())

def category(request):
    try:
        # 先获取客户端提交的信息
        cid = request.GET.get('cid', None)
        try:
            category = Category.objects.get(pk=cid)
        except Category.DoesNotExist:
            return render(request, 'failure.html', {'reason': '分类不存在'})
        article_list = Article.objects.filter(category=category)
        article_list = getPage(request, article_list)
    except Exception as e:
        logger.error(e)
    return render(request, 'category.html', locals())