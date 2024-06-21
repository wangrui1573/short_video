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
