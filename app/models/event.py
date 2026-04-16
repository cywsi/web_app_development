from app.models.db import get_db_connection

class EventModel:
    @staticmethod
    def create(title, description, start_time, end_time, capacity):
        """
        新增一筆活動記錄。
        參數：
          - title: 活動名稱
          - description: 活動簡述
          - start_time: 開始時間
          - end_time: 結束時間
          - capacity: 人數上限
        回傳：
          - 新增記錄的 ID
        """
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO event (title, description, start_time, end_time, capacity)
                VALUES (?, ?, ?, ?, ?)
            ''', (title, description, start_time, end_time, capacity))
            conn.commit()
            last_id = cursor.lastrowid
            return last_id
        except Exception as e:
            print(f"Error creating event: {e}")
            conn.rollback()
            raise e
        finally:
            conn.close()

    @staticmethod
    def get_all():
        """
        取得所有活動記錄，並包含目前已報名的人數(booked_count)。
        回傳：
          - 字典列表 [{ 'id': ... , 'title': ... }, ...]
        """
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT e.*, 
                       (SELECT COUNT(id) FROM registration WHERE event_id = e.id) as booked_count 
                FROM event e 
                ORDER BY e.created_at DESC
            ''')
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        except Exception as e:
            print(f"Error getting all events: {e}")
            raise e
        finally:
            conn.close()

    @staticmethod
    def get_by_id(event_id):
        """
        依據 ID 取得單筆活動記錄，並包含目前已報名的人數(booked_count)。
        參數：
          - event_id: 活動 ID
        回傳：
          - 字典，若找不到則回傳 None
        """
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT e.*, 
                       (SELECT COUNT(id) FROM registration WHERE event_id = e.id) as booked_count 
                FROM event e 
                WHERE e.id = ?
            ''', (event_id,))
            row = cursor.fetchone()
            return dict(row) if row else None
        except Exception as e:
            print(f"Error getting event by id {event_id}: {e}")
            raise e
        finally:
            conn.close()

    @staticmethod
    def update(event_id, title, description, start_time, end_time, capacity):
        """
        依據 ID 更新活動記錄。
        參數：
          - event_id: 活動 ID
          - title, description, start_time, end_time, capacity: 要更新的資料
        回傳：
          - 布林值，更新成功回傳 True，否則 False
        """
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE event 
                SET title = ?, description = ?, start_time = ?, end_time = ?, capacity = ?
                WHERE id = ?
            ''', (title, description, start_time, end_time, capacity, event_id))
            conn.commit()
            updated = cursor.rowcount > 0
            return updated
        except Exception as e:
            print(f"Error updating event {event_id}: {e}")
            conn.rollback()
            raise e
        finally:
            conn.close()

    @staticmethod
    def delete(event_id):
        """
        依據 ID 刪除一筆活動記錄。
        參數：
          - event_id: 活動 ID
        回傳：
          - 布林值，刪除成功回傳 True，否則 False
        """
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM event WHERE id = ?', (event_id,))
            conn.commit()
            deleted = cursor.rowcount > 0
            return deleted
        except Exception as e:
            print(f"Error deleting event {event_id}: {e}")
            conn.rollback()
            raise e
        finally:
            conn.close()
