# database.py
# 用于与数据库进行交互

import sqlite3

# 初始化数据库
def init_db():
    conn = sqlite3.connect('media.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS media
                 (id INTEGER PRIMARY KEY, name TEXT, path TEXT, views INTEGER DEFAULT 0, likes INTEGER DEFAULT 0)''')
    conn.commit()
    conn.close()

# 添加媒体到数据库
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

# 更新媒体的访问次数
def update_views(media_id):
    conn = sqlite3.connect('media.db')
    c = conn.cursor()
    c.execute("UPDATE media SET views = views + 1 WHERE id = ?", (media_id,))
    conn.commit()
    conn.close()

# 更新媒体的点赞次数
def update_likes(media_id):
    conn = sqlite3.connect('media.db')
    c = conn.cursor()
    c.execute("UPDATE media SET likes = likes + 1 WHERE id = ?", (media_id,))
    conn.commit()
    conn.close()

# 删除媒体
def delete_media(media_id):
    conn = sqlite3.connect('media.db')
    c = conn.cursor()
    c.execute("DELETE FROM media WHERE id = ?", (media_id,))
    conn.commit()
    conn.close()

# 获取随机媒体
def get_random_media():
    conn = sqlite3.connect('media.db')
    c = conn.cursor()
    c.execute("SELECT id, name, path FROM media ORDER BY RANDOM() LIMIT 1")
    media = c.fetchone()
    conn.close()
    return media
