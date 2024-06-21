



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
- [x] 在网页上 点赞和删除文件
- [x] 上下滑动来切换文件
- [x] 媒体文件放在video目录下
- [x] 本地数据库





### 代码由4个文件组成



#### 1.数据库操作

```
# database.py

import sqlite3

def init_db():
    conn = sqlite3.connect('media.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS media
                 (id INTEGER PRIMARY KEY, name TEXT, path TEXT, views INTEGER DEFAULT 0, likes INTEGER DEFAULT 0)''')
    conn.commit()
    conn.close()

def add_media(name, path):
    try:
        conn = sqlite3.connect('media.db')
        c = conn.cursor()
        c.execute("INSERT INTO media (name, path) VALUES (?, ?)", (name, path))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        # 处理重复键错误等数据库约束错误
        return False
    except Exception as e:
        print(f"Error inserting {name} into database: {str(e)}")
        return False

def update_views(media_id):
    conn = sqlite3.connect('media.db')
    c = conn.cursor()
    c.execute("UPDATE media SET views = views + 1 WHERE id = ?", (media_id,))
    conn.commit()
    conn.close()

def update_likes(media_id):
    conn = sqlite3.connect('media.db')
    c = conn.cursor()
    c.execute("UPDATE media SET likes = likes + 1 WHERE id = ?", (media_id,))
    conn.commit()
    conn.close()

def delete_media(media_id):
    conn = sqlite3.connect('media.db')
    c = conn.cursor()
    c.execute("DELETE FROM media WHERE id = ?", (media_id,))
    conn.commit()
    conn.close()

def get_random_media():
    conn = sqlite3.connect('media.db')
    c = conn.cursor()
    c.execute("SELECT id, name, path FROM media ORDER BY RANDOM() LIMIT 1")
    media = c.fetchone()
    conn.close()
    return media

```



#### 2.文件扫描

```
#scanner.py
import os
import time
import sqlite3
from database import init_db, add_media

def scan_directory(directory='video'):
    init_db()
    print(f"扫描目录: {directory}")
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(('.mp4', '.jpg', '.png', '.gif')):
                path = os.path.join(root, file)
                print(f"发现文件: {file} 路径: {path}")
                try:
                    result = add_media(file, path)
                    #print(f"add_media 返回: {result}")  # Debug: Print the return value
                    if result:
                        print(f"插入 {file} 到数据库")
                    else:
                        print(f"插入 {file} 到数据库失败")
                except Exception as e:
                    print(f"由于异常无法插入 {file} 到数据库: {str(e)}")

def incremental_scan(directory='video'):
    scanned_files = set()
    conn = sqlite3.connect('media.db')
    c = conn.cursor()
    c.execute("SELECT path FROM media")
    for row in c.fetchall():
        scanned_files.add(row[0])
    conn.close()

    print("开始增量扫描...")
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(('.mp4', '.jpg', '.png', '.gif')):
                path = os.path.join(root, file)
                if path not in scanned_files:
                    print(f"发现新文件: {file} 路径: {path}")
                    try:
                        result = add_media(file, path)
                        print(f"add_media 返回: {result}")  # Debug: Print the return value
                        if result:
                            print(f"插入 {file} 到数据库")
                        else:
                            print(f"插入 {file} 到数据库失败")
                    except Exception as e:
                        print(f"由于异常无法插入 {file} 到数据库: {str(e)}")
                else:
                    print(f"跳过已存在文件: {file}")

if __name__ == '__main__':
    init_db()
    while True:
        incremental_scan()
        time.sleep(3600)  # 每小时扫描一次

```



#### 3.web服务

```
#app.py

from flask import Flask, render_template, request, send_file, jsonify, send_from_directory
import os
import sqlite3
import random  # 导入 random 模块
from database import init_db, update_views, update_likes, delete_media, get_random_media

app = Flask(__name__)

def is_video_file(path):
    return path.lower().endswith('.mp4')

def is_image_file(path):
    return path.lower().endswith('.jpg') or path.lower().endswith('.jpeg') or path.lower().endswith('.png')

def get_random_media():
    conn = sqlite3.connect('media.db')
    c = conn.cursor()

    rand_num = random.random()  # Generate a random number between 0 and 1
    if rand_num < 0.9:
        c.execute("SELECT id, name, path FROM media WHERE path LIKE '%.mp4' ORDER BY RANDOM() LIMIT 1;")
    else:
        c.execute("SELECT id, name, path FROM media WHERE path LIKE '%.jpg' OR path LIKE '%.jpeg' OR path LIKE '%.png' ORDER BY RANDOM() LIMIT 1;")

    media = c.fetchone()

    conn.close()
    return media

@app.route('/')
def index():
    media = get_random_media()
    if media:
        media_id, name, path = media
        update_views(media_id)
        conn = sqlite3.connect('media.db')
        c = conn.cursor()
        c.execute("SELECT likes FROM media WHERE id = ?", (media_id,))
        likes = c.fetchone()[0]
        conn.close()
        return render_template('index.html', media_id=media_id, name=name, path=path, likes=likes,
                               is_video=is_video_file(path), is_image=is_image_file(path))
    return "No media found"

@app.route('/media/<path:filename>')
def media(filename):
    return send_from_directory(directory=os.path.dirname(filename), path=os.path.basename(filename))

@app.route('/like/<int:media_id>', methods=['POST'])
def like(media_id):
    update_likes(media_id)
    conn = sqlite3.connect('media.db')
    c = conn.cursor()
    c.execute("SELECT likes FROM media WHERE id = ?", (media_id,))
    likes = c.fetchone()[0]
    conn.close()
    return jsonify(success=True, likes=likes)

@app.route('/delete/<int:media_id>', methods=['POST'])
def delete(media_id):
    conn = sqlite3.connect('media.db')
    c = conn.cursor()
    c.execute("SELECT path FROM media WHERE id = ?", (media_id,))
    path = c.fetchone()[0]
    conn.close()
    if os.path.exists(path):
        os.remove(path)
    delete_media(media_id)
    return jsonify(success=True)

@app.route('/download/<int:media_id>')
def download(media_id):
    conn = sqlite3.connect('media.db')
    c = conn.cursor()
    c.execute("SELECT path FROM media WHERE id = ?", (media_id,))
    path = c.fetchone()[0]
    conn.close()
    return send_file(path, as_attachment=True)

if __name__ == '__main__':
    init_db()  # 确保数据库和表被初始化
    app.run(host='0.0.0.0', port=3000, debug=True)

```



#### 4.启动器

```
import os
import threading
import time

# 定义运行scanner.py的函数
def run_scanner():
    # 清空并创建scanner.log文件
    with open('log/scanner.log', 'wb') as f:
        pass
    os.system('python scanner.py > log/scanner.log 2>&1')

# 定义运行app.py的函数
def run_app():
    # 清空并创建app.log文件
    with open('log/app.log', 'wb') as f:
        pass
    os.system('python app.py > log/app.log 2>&1')

if __name__ == '__main__':
    # 创建log子目录
    os.makedirs('log', exist_ok=True)

    # 创建并启动线程运行scanner.py
    scanner_thread = threading.Thread(target=run_scanner)
    scanner_thread.start()

    # 等待3秒钟
    time.sleep(3)

    # 创建并启动线程运行app.py
    app_thread = threading.Thread(target=run_app)
    app_thread.start()

```

