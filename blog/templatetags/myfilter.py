# -*- coding:utf-8 -*-
import logging
from django import template
register = template.Library()

# Initial a logger handler
logger = logging.getLogger("blog.views")


# 定义一个将日期中的月份转换为中文月份的过滤器，如：1转换为一
@register.filter
def month_to_upper(key):
    try:
        month_upper_list = ['一','二','三','四','五','六','七','八','九','十','十一','十二']
        return month_upper_list[key.month-1]
    except Exception as e:
        logger.error(e)
    return key.month


# 注册过滤器
#register.filter('month_to_upper',month_to_upper)
