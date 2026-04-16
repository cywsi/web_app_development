from app.models.db import get_db_connection

class EventModel:
    @staticmethod
    def create(title, description, start_time, end_time, capacity):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO event (title, description, start_time, end_time, capacity)
            VALUES (?, ?, ?, ?, ?)
        ''', (title, description, start_time, end_time, capacity))
        conn.commit()
        last_id = cursor.lastrowid
        conn.close()
        return last_id

    @staticmethod
    def get_all():
        conn = get_db_connection()
        cursor = conn.cursor()
        # 列出所有活動，並同時計算已報名人數
        cursor.execute('''
            SELECT e.*, 
                   (SELECT COUNT(id) FROM registration WHERE event_id = e.id) as booked_count 
            FROM event e 
            ORDER BY e.created_at DESC
        ''')
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    @staticmethod
    def get_by_id(event_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        # 取得單一活動資訊，同時包含目前報名人數
        cursor.execute('''
            SELECT e.*, 
                   (SELECT COUNT(id) FROM registration WHERE event_id = e.id) as booked_count 
            FROM event e 
            WHERE e.id = ?
        ''', (event_id,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None

    @staticmethod
    def update(event_id, title, description, start_time, end_time, capacity):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE event 
            SET title = ?, description = ?, start_time = ?, end_time = ?, capacity = ?
            WHERE id = ?
        ''', (title, description, start_time, end_time, capacity, event_id))
        conn.commit()
        updated = cursor.rowcount > 0
        conn.close()
        return updated

    @staticmethod
    def delete(event_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM event WHERE id = ?', (event_id,))
        conn.commit()
        deleted = cursor.rowcount > 0
        conn.close()
        return deleted
