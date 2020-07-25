更多文档参考[docs文件夹](docs/)

# preview

![img](docs/preview/0.0.1.gif)

# featrue

自动监听鼠标所在位置

自动推断当前鼠标所处于的顶层程序信息

自动推断当前数据所在的程序的顶层控件句柄信息

# standard

分为两层:

程序

控件



程序:

path, title

控件:

class_name, title, index



通过 程序(path,title) 找到顶层控件

循环遍历控件列表进入控件内部找到末端控件

对末端控件进行操作



类似xpath

# dev

python 版本: 3.7

安装依赖库:

pip install -r requirements.txt



导出本地依赖文件清单到文件:

pip freeze > requirements.txt



运行 setup.py

# bugs

## 严重的性能问题

## 严重的稳定性问题