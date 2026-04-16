from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.event import EventModel
from app.models.registration import RegistrationModel

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """首頁活動列表"""
    try:
        events = EventModel.get_all()
        return render_template('index.html', events=events)
    except Exception as e:
        flash(f"資料載入失敗：{e}", "danger")
        return render_template('index.html', events=[])

@main_bp.route('/events/create', methods=['GET'])
def create_event_page():
    """顯示建立活動表單"""
    return render_template('create.html')

@main_bp.route('/events/create', methods=['POST'])
def create_event():
    """處理建立活動表單提交"""
    title = request.form.get('title', '').strip()
    description = request.form.get('description', '').strip()
    start_time = request.form.get('start_time', '').strip()
    end_time = request.form.get('end_time', '').strip()
    capacity_str = request.form.get('capacity', '').strip()

    # 必填驗證
    if not title or not start_time or not end_time or not capacity_str:
        flash('請填寫所有必填欄位（名稱、時間、人數上限）', 'danger')
        return render_template('create.html', 
                               title=title, description=description, 
                               start_time=start_time, end_time=end_time, 
                               capacity=capacity_str)
    
    # 數字格式驗證
    try:
        capacity = int(capacity_str)
        if capacity <= 0:
            raise ValueError()
    except ValueError:
        flash('人數上限必須是正整數', 'danger')
        return render_template('create.html', 
                               title=title, description=description, 
                               start_time=start_time, end_time=end_time, 
                               capacity=capacity_str)

    # 嘗試寫入資料庫
    try:
        event_id = EventModel.create(title, description, start_time, end_time, capacity)
        flash('活動建立成功！', 'success')
        return redirect(url_for('main.event_detail', id=event_id))
    except Exception as e:
        flash(f'活動建立失敗：{e}', 'danger')
        return render_template('create.html', 
                               title=title, description=description, 
                               start_time=start_time, end_time=end_time, 
                               capacity=capacity_str)

@main_bp.route('/events/<int:id>', methods=['GET'])
def event_detail(id):
    """顯示單一活動詳情與報名表單"""
    try:
        event = EventModel.get_by_id(id)
        if not event:
            flash('找不到該活動，可能已經被刪除', 'danger')
            return redirect(url_for('main.index'))
        return render_template('detail.html', event=event)
    except Exception as e:
        flash(f'系統錯誤：{e}', 'danger')
        return redirect(url_for('main.index'))

@main_bp.route('/events/<int:id>/register', methods=['POST'])
def register_event(id):
    """處理報名表單提交"""
    user_name = request.form.get('user_name', '').strip()
    user_email = request.form.get('user_email', '').strip()
    user_phone = request.form.get('user_phone', '').strip()

    # 基本資料驗證
    if not user_name or not user_email:
        flash('請填寫必填欄位（姓名、Email）以供報名', 'danger')
        return redirect(url_for('main.event_detail', id=id))

    # 嘗試報名
    try:
        RegistrationModel.create(id, user_name, user_email, user_phone)
        flash('報名成功！感謝您的參與', 'success')
    except ValueError as e:
        # 捕捉 Model 拋出的業務邏輯錯誤 (如額滿)
        flash(f'報名失敗：{e}', 'danger')
    except Exception as e:
        # 其他資料庫或未預期錯誤
        flash('系統發生未預期的錯誤，報名失敗，請稍後再試。', 'danger')
        
    return redirect(url_for('main.event_detail', id=id))
