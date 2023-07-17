from watchlist import app
from flask import render_template


# 404 页面错误处理
@app.errorhandler(404)   # 要处理的错误代码
def page_not_find(e):  # 接受异常对象作为参数
    # user = User.query.first()
    # return render_template('404.html', user=user), 404  # 返回模板和状态码
    return render_template('errors/404.html'), 404  # 返回模板和状态码
"""
和我们前面编写的视图函数相比，这个函数返回了状态码作为第二个参数，普通的视图函数之所以不用写出状态码，是因为默认会使用 200 状态码，表示成功
"""