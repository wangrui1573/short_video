# 使用官方的 Python 基础镜像，选择轻量的 alpine 版本
FROM python:3.9-alpine

# 设置工作目录为 /app
WORKDIR /app

# 复制当前目录中的所有文件到 /app 目录
COPY . .

# 如果需要安装依赖，请将 requirements.txt 放置在 /app 目录下，并取消注释以下行
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# 暴露端口 3000
EXPOSE 3000

# 设置入口命令，同时启动 scanner.py 和 app.py
CMD ["sh", "-c", "python scanner.py & python app.py"]
