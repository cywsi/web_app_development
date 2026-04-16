from app.models.db import get_db_connection

class RegistrationModel:
    @staticmethod
    def create(event_id, user_name, user_email, user_phone=''):
        conn = get_db_connection()
        try:
            # 開啟交易 (Transaction) 以進行併發控制
            conn.execute("BEGIN IMMEDIATE TRANSACTION")
            cursor = conn.cursor()
            
            # 取得活動名額與目前已報名人數
            cursor.execute('''
                SELECT capacity, 
                       (SELECT COUNT(id) FROM registration WHERE event_id = ?) as booked
                FROM event 
                WHERE id = ?
            ''', (event_id, event_id))
            
            row = cursor.fetchone()
            if not row:
                raise ValueError("活動不存在")
                
            # 檢查是否已額滿
            if row['booked'] >= row['capacity']:
                raise ValueError("活動名額已滿")
                
            # 寫入報名資料
            cursor.execute('''
                INSERT INTO registration (event_id, user_name, user_email, user_phone)
                VALUES (?, ?, ?, ?)
            ''', (event_id, user_name, user_email, user_phone))
            
            conn.commit()
            last_id = cursor.lastrowid
            return last_id
            
        except Exception as e:
            # 發生任何錯誤（包括額滿），就 Rollback 復原資料庫變更
            conn.rollback()
            raise e
        finally:
            conn.close()

    @staticmethod
    def get_all_by_event(event_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM registration 
            WHERE event_id = ? 
            ORDER BY created_at ASC
        ''', (event_id,))
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
        
    @staticmethod
    def get_by_id(reg_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM registration WHERE id = ?", (reg_id,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None
        
    @staticmethod
    def delete(reg_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM registration WHERE id = ?', (reg_id,))
        conn.commit()
        deleted = cursor.rowcount > 0
        conn.close()
        return deleted
