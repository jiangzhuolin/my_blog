# -*- coding:utf-8 -*-
from django.shortcuts import render
import logging
from django.conf import settings # 导入settings
from blog.models import *
from django.core.paginator import Paginator,InvalidPage,EmptyPage,PageNotAnInteger
from django.db import connection
from django.db.models import Count


# Create your views here.
# Initial a logger handler
logger = logging.getLogger("blog.views")

# 定义一个方法，返回 settings 文件中的内容
def global_setting(request):
    SITE_NAME=settings.SITE_NAME
    SITE_DESC = settings.SITE_DESC
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
    return render(request,'article.html',locals())