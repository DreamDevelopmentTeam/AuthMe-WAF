# 导入Flask模块和waf模块
from flask import Flask, request
from waf import waf

# 创建一个Flask应用对象
app = Flask(__name__)

# 定义一个路由，用于处理GET和POST请求
@app.route("/", methods=["GET", "POST"])
def index():
    # 如果是GET请求，直接返回一个HTML字符串，包含一个表单，让用户输入参数
    if request.method == "GET":
        return """
        <html>
        <head>
        <title>Flask示例</title>
        </head>
        <body>
        <h1>请输入你的信息</h1>
        <form method="POST" action="/">
        <p>姓名：<input type="text" name="name"></p>
        <p>邮箱：<input type="email" name="email"></p>
        <p>留言：<textarea name="message"></textarea></p>
        <p><input type="submit" value="提交"></p>
        </form>
        </body>
        </html>
        """
    # 如果是POST请求，获取用户输入的参数，并调用waf函数判断是否有攻击关键字
    elif request.method == "POST":
        # 获取用户输入的参数
        name = request.form.get("name")
        email = request.form.get("email")
        message = request.form.get("message")
        # 调用waf函数，传入request对象，返回布尔值
        result = waf(request)
        # 如果返回True，表示请求中包含攻击关键字，直接返回一个HTML字符串，包含一个警告信息，提示用户不要尝试攻击
        if result:
            return """
            <html>
            <head>
            <title>Flask示例</title>
            </head>
            <body>
            <h1>警告！</h1>
            <p>你的请求中包含SQL注入或XSS攻击的关键字，请不要尝试攻击本站。</p>
            </body>
            </html>
            """
        # 如果返回False，表示请求中没有攻击关键字，直接返回一个HTML字符串，包含一个感谢信息，显示用户输入的参数
        else:
            return f"""
            <html>
            <head>
            <title>Flask示例</title>
            </head>
            <body>
            <h1>感谢你的提交</h1>
            <p>你输入的信息如下：</p>
            <ul>
            <li>姓名：{name}</li>
            <li>邮箱：{email}</li>
            <li>留言：{message}</li>
            </ul>
            </body>
            </html>
            """

# 运行Flask应用
if __name__ == "__main__":
    app.run()
