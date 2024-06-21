



## 本地短视频服务器



> 背景：我的NAS中存放了很多短视频，多到很多没看过，于是写了这个程序来随机查看并删除短视频



### 运行：

> 安装依赖后运行main.py
>
> 直接使用docker：
>
> docker pull realwang/short_video
>
> docker run -d -p 3000:3000 -v /path/to/your/video:/app/video realwang/short_video





### 功能

- [x] 扫描本地视频和图片，并在网页上显示
- [x] 可以在网页上 点赞和删除文件
- [x] 媒体文件放在video目录下
- [x] 本地数据库