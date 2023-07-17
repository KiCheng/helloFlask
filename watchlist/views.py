from watchlist import app, db
from watchlist.models import User, Movie
from flask import render_template
from flask import url_for, request, flash, redirect
from flask_login import login_user, login_required, logout_user, current_user


# 主页
@app.route('/', methods=['GET', 'POST'])  # 默认只接受 GET 请求，上面的写法表示同时接受 GET 和 POST 请求
def index():
    """ Add data... """
    if request.method == 'POST':
        if not current_user.is_authenticated:  # 如果当前登录未认证
            return redirect(url_for('index'))
        # 获取表单数据
        title = request.form.get("title")
        year = request.form.get("year")
        # 验证数据
        if not title or not year or len(title) > 60 or len(year) > 4:
            flash("Invalid Input...")
            return redirect(url_for('index'))  # 重定向
        # 保存数据到数据库
        movie = Movie(title=title, year=year)
        db.session.add(movie)
        db.session.commit()
        flash("Add to db...")
        return redirect(url_for('index'))
    # user = User.query.first()
    movies = Movie.query.all()
    # return render_template('index.html', user=user, movies=movies)
    return render_template('index.html', movies=movies)


# 设置：修改用户的名字
@app.route("/settings", methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        """
        Flask-Login 提供了一个 current_user 变量，当程序运行后，如果用户已登录，current_user 变量的值会是当前用户的用户模型类记录。
        """
        name = request.form.get("name")
        if not name or len(name) > 20:
            flash("Invalid input...")
            return redirect(url_for('index'))
        # 修改用户的name字段值
        current_user.name = name
        db.session.commit()
        flash("Update name Done!")
        return redirect(url_for('index'))
    return render_template('settings.html')


# 登录功能
@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")
        if not username or not password:
            # 用户名或密码未填写
            flash("Username or Password is Empty...")
            return redirect(url_for('login'))
        # 进行用户名和密码的校验
        user = User.query.filter(User.username == username).first()
        if user is None:
            # 用户名不存在，无法登录
            flash("Username is not existed...")
            return redirect(url_for('login'))
        else:
            # 用户名存在，校验密码
            status = user.validate_password(password)
            if status is True:
                flash("Login Done!")
                login_user(user)  # 登入用户
                return redirect(url_for('index'))
            else:
                flash("Password Error...")
                return redirect(url_for('login'))
    return render_template('login.html')


# 登出功能
@app.route("/logout")
@login_required  # 用于视图保护，后面会详细介绍
def logout():
    logout_user()  # 用户登出
    flash("GoodBye...")
    return redirect(url_for('index'))


# 修改表单数据
@app.route("/movie/edit/<int:movie_id>", methods=['GET', 'POST'])
@login_required  # 页面保护（相当于java的filter）
def edit(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    if request.method == 'POST':
        title = request.form.get("title")
        year = request.form.get("year")
        if not title or not year or len(year) != 4 or len(title) > 60:
            flash("Input Invalid...")
            return redirect(url_for('edit', movie_id=movie_id))
        # 更新数据库
        movie.title = title
        movie.year = year
        db.session.commit()
        flash("Update in db...")
        return redirect(url_for('index'))
    # 数据回显
    return render_template('edit.html', movie=movie)


# 电影数据删除
@app.route("/movie/delete/<int:movie_id>", methods=['POST'])
@login_required
def delete(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    # 调用数据库将其删除
    db.session.delete(movie)
    db.session.commit()
    flash("Delete Done...")
    # 回显到index页面
    return redirect(url_for('index'))