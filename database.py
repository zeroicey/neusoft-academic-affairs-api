import sqlite3
import datetime
from typing import Optional


class DatabaseManager:
    def __init__(self, db_path: str = "./database.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """初始化数据库，创建cookie存储表"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 创建cookie存储表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_cookies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                stu_num TEXT UNIQUE NOT NULL,
                stu_pwd TEXT NOT NULL,
                cookie TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_valid BOOLEAN DEFAULT 1
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def save_cookie(self, stu_num: str, stu_pwd: str, cookie: str):
        """保存用户cookie到数据库"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 使用REPLACE来更新或插入
        cursor.execute('''
            REPLACE INTO user_cookies (stu_num, stu_pwd, cookie, updated_at, is_valid)
            VALUES (?, ?, ?, datetime('now'), 1)
        ''', (stu_num, stu_pwd, cookie))
        
        conn.commit()
        conn.close()
    
    def get_valid_cookie(self, stu_num: str) -> Optional[str]:
        """获取有效的cookie"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT cookie FROM user_cookies 
            WHERE stu_num = ? AND is_valid = 1
        ''', (stu_num,))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return result[0]
        
        return None
    
    def invalidate_cookie(self, stu_num: str):
        """将cookie标记为无效"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE user_cookies SET is_valid = 0 
            WHERE stu_num = ?
        ''', (stu_num,))
        
        conn.commit()
        conn.close()
    
    def cleanup_expired_cookies(self):
        """清理无效的cookie记录"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            DELETE FROM user_cookies 
            WHERE is_valid = 0
        ''')
        
        conn.commit()
        conn.close()