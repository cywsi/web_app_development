from app.models.db import get_db_connection

class RegistrationModel:
    @staticmethod
    def create(event_id, user_name, user_email, user_phone=''):
        """
        新增一筆報名記錄，並利用 Transaction 驗證名額是否已滿。
        參數：
          - event_id: 欲報名的活動 ID
          - user_name: 報名者姓名
          - user_email: 報名者 Email
          - user_phone: 報名者聯絡電話
        回傳：
          - 成功新增的報名記錄 ID
        例外：
          - 若活動不存在或名額已滿，則拋出 ValueError
        """
        conn = get_db_connection()
        try:
            conn.execute("BEGIN IMMEDIATE TRANSACTION")
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT capacity, 
                       (SELECT COUNT(id) FROM registration WHERE event_id = ?) as booked
                FROM event 
                WHERE id = ?
            ''', (event_id, event_id))
            
            row = cursor.fetchone()
            if not row:
                raise ValueError("活動不存在")
                
            if row['booked'] >= row['capacity']:
                raise ValueError("活動名額已滿")
                
            cursor.execute('''
                INSERT INTO registration (event_id, user_name, user_email, user_phone)
                VALUES (?, ?, ?, ?)
            ''', (event_id, user_name, user_email, user_phone))
            
            conn.commit()
            last_id = cursor.lastrowid
            return last_id
            
        except Exception as e:
            conn.rollback()
            print(f"Error creating registration: {e}")
            raise e
        finally:
            conn.close()

    @staticmethod
    def get_all():
        """
        取得系統內所有的報名記錄。
        回傳：
          - 字典列表
        """
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM registration ORDER BY created_at ASC")
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        except Exception as e:
            print(f"Error getting all registrations: {e}")
            raise e
        finally:
            conn.close()

    @staticmethod
    def get_all_by_event(event_id):
        """
        取得特定活動底下的所有報名記錄。
        參數：
          - event_id: 活動 ID
        回傳：
          - 字典列表
        """
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM registration 
                WHERE event_id = ? 
                ORDER BY created_at ASC
            ''', (event_id,))
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        except Exception as e:
            print(f"Error getting registrations for event {event_id}: {e}")
            raise e
        finally:
            conn.close()
        
    @staticmethod
    def get_by_id(reg_id):
        """
        依據 ID 取得單筆報名記錄。
        參數：
          - reg_id: 報名記錄 ID
        回傳：
          - 字典，找不到則回傳 None
        """
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM registration WHERE id = ?", (reg_id,))
            row = cursor.fetchone()
            return dict(row) if row else None
        except Exception as e:
            print(f"Error getting registration {reg_id}: {e}")
            raise e
        finally:
            conn.close()

    @staticmethod
    def update(reg_id, user_name, user_email, user_phone):
        """
        更新報名記錄。
        參數：
          - reg_id: 報名記錄 ID
          - user_name, user_email, user_phone: 欲更新的聯絡資料
        回傳：
          - 布林值，成功為 True
        """
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE registration
                SET user_name = ?, user_email = ?, user_phone = ?
                WHERE id = ?
            ''', (user_name, user_email, user_phone, reg_id))
            conn.commit()
            updated = cursor.rowcount > 0
            return updated
        except Exception as e:
            print(f"Error updating registration {reg_id}: {e}")
            conn.rollback()
            raise e
        finally:
            conn.close()
        
    @staticmethod
    def delete(reg_id):
        """
        依據 ID 刪除一筆報名記錄。
        參數：
          - reg_id: 報名記錄 ID
        回傳：
          - 刪除成功回傳 True，否則 False
        """
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM registration WHERE id = ?', (reg_id,))
            conn.commit()
            deleted = cursor.rowcount > 0
            return deleted
        except Exception as e:
            print(f"Error deleting registration {reg_id}: {e}")
            conn.rollback()
            raise e
        finally:
            conn.close()
