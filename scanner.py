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
