# 导入相关模块
import re
from fastapi import Request
from flask import request as flask_request

# 定义正则表达式，用于匹配SQL注入和XSS攻击的关键字
# sql_injection_pattern = re.compile(r"(\bunion\b|\bselect\b|\bfrom\b|\bwhere\b|\bdrop\b|\bdelete\b|\bupdate\b|\binsert\b|\binto\b|\bexec\b|\bsp_\w+)|(\-\-|\'\s*or\s*\d+=\d+|\'\s*and\s*\d+=\d+|\'\s*or\s*\w+=\w+|\'\s*and\s*\w+=\w+)", re.IGNORECASE)
# xss_attack_pattern = re.compile(r"(alert\(|<style|</style|<script|</script|<script>|</script>|<img|<iframe|<div|<style>|</style>|<link|<meta|<body|onload=|onerror=|onclick=|onmouseover=)", re.IGNORECASE)
# sql_injection_pattern = re.compile(r"(\bunion\b|\bselect\b|\bfrom\b|\bwhere\b|\bdrop\b|\bdelete\b|\bupdate\b|\binsert\b|\binto\b|\bexec\b|\bsp_\w+|\bconcat\b|\bsubstring\b|\buser\b|\bdatabase\b|\bversion\b)|(\-\-|\'\s*or\s*\d+=\d+|\'\s*and\s*\d+=\d+|\'\s*or\s*\w+=\w+|\'\s*and\s*\w+=\w+|%00|%0a|%0d)", re.IGNORECASE)
sql_injection_pattern = re.compile(r"(\bunion\b|\bselect\b|\bfrom\b|\bwhere\b|\bdrop\b|\bdelete\b|\bupdate\b|\binsert\b|\binto\b|\bexec\b|\bsp_\w+|\bconcat\b|\bsubstring\b|\buser\b|\bdatabase\b|\bversion\b)|(\-\-|\'\s*or\s*\d+=\d+|\'\s*and\s*\d+=\d+|\'\s*or\s*\w+=\w+|\'\s*and\s*\w+=\w+|%00|%0a|%0d)|(\s*=\s*|<|>|!|~)\s*(\d+|\'\w+\')", re.IGNORECASE)
xss_attack_pattern = re.compile(r"(alert\(|<style|style>|</style|<script|</script|script>|<script>|</script>|<img|<iframe|<div|<style>|</style>|<link|<meta|<body|onload=|onerror=|onclick=|onmouseover=|onfocus=|onblur=|oninput=|onkeydown=|onkeyup=|onkeypress=|onsubmit=|onreset=|onselect=|onchange=|src=|href=|%3c|%3e)", re.IGNORECASE)

ip_black_list = [

]

# 定义一个函数，用于判断请求对象是否是FastAPI的Request类的实例
def is_fastapi_request(request):
    return isinstance(request, Request)

# 定义一个函数，用于判断请求对象是否是Flask的request对象
def is_flask_request(request):
    return request == flask_request

# 定义一个函数，用于获取请求对象的所有参数（包括URL参数和表单参数）
def get_all_params(request):
    params = {}
    if is_fastapi_request(request):
        # 如果是FastAPI的Request类的实例，使用query_params和form方法获取参数
        params.update(request.query_params)
        params.update(request.form)
    elif is_flask_request(request):
        # 如果是Flask的request对象，使用args和form属性获取参数
        params.update(request.args)
        params.update(request.form)
    return params

# 定义一个函数，用于判断请求中是否包含SQL注入或XSS攻击的关键字
def has_attack_keyword(request):
    # 获取请求对象的所有参数
    params = get_all_params(request)
    # 遍历所有参数的值，如果匹配到SQL注入或XSS攻击的正则表达式，返回True
    for value in params.values():
        if sql_injection_pattern.search(value) or xss_attack_pattern.search(value):
            return True
    # 如果没有匹配到任何关键字，返回False
    return False

# 定义一个函数，用于适配FastAPI和Flask框架，传入请求对象，返回布尔值，表示请求中是否包含SQL注入或XSS攻击字段
def waf(request):
    # 如果请求对象是FastAPI的Request类的实例或Flask的request对象，调用has_attack_keyword函数判断是否有攻击关键字
    if is_fastapi_request(request) or is_flask_request(request):
        return has_attack_keyword(request)
    # 如果请求对象不是以上两种类型，抛出异常
    else:
        raise TypeError("Unsupported request type")
