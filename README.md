# Flask快速入门
在本地完成开发，将项目部署到云服务器上。
![image](https://github.com/KiCheng/helloFlask/assets/108656173/062c6e04-79e2-41e1-ab0b-e399faf61ac9)

## Installation

项目根目录：

```shell
cd watchlist
```

创建虚拟环境：

```shell
python3 -m venv 虚拟环境名称
```

激活虚拟环境：

```shell
source 虚拟环境名称/bin/activate
```

安装项目所需依赖：

```shell
pip install -r requirements.txt
```

创建数据库架构和虚拟数据：

```shell
flask initdb  # 初始化数据库
flask forge  # 创建数据
flask run  # 运行服务器  http://127.0.0.1:5000/
```

不使用Flask自带的服务器，将项目部署到云服务器上：

可参考https://www.pythonanywhere.com.
