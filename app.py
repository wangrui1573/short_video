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
