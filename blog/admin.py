# -*- coding:utf-8 -*-
from django.contrib import admin
from blog.models import *

# Register your models here.


class ArticleAdmin(admin.ModelAdmin):
    # 后台列表项所展示的字段
    list_display = ('title','desc','category','click_count','date_publish')
    # 后台列表项所展示的字段中可点击链接字段
    list_display_links = ('title','desc','category')
    # 后台列表项所展示的字段中可编辑字段
    list_editable = ('click_count',)
    fieldsets= (
        (None,{
            'fields':('title','desc','content',)
        }),
        ('高级设置',{
            'classes':('collapse',),
            'fields': ('click_count','is_recommend','category','tag','user')
        }),
    )

    class Media:
        js = (
            '/static/js/kindeditor-4.1.10/kindeditor-min.js',
            '/static/js/kindeditor-4.1.10/lang/zh_CN.js',
            '/static/js/kindeditor-4.1.10/config.js',
        )


admin.site.register(User)
admin.site.register(Article,ArticleAdmin)
admin.site.register(Tag)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Links)
admin.site.register(Ad)