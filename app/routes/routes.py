from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.event import EventModel
from app.models.registration import RegistrationModel

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """
    HTTP GET: /
    首頁活動列表。
    呼叫 EventModel.get_all() 獲取資料，並渲染 index.html。
    """
    pass

@main_bp.route('/events/create', methods=['GET'])
def create_event_page():
    """
    HTTP GET: /events/create
    顯示建立活動表單。
    負責渲染 create.html。
    """
    pass

@main_bp.route('/events/create', methods=['POST'])
def create_event():
    """
    HTTP POST: /events/create
    處理建立活動表單提交。
    取得 request.form 內的資料後呼叫 EventModel.create()，
    成功後 flash 成功訊息，並重新導向 (redirect) 至首頁或詳情頁。
    """
    pass

@main_bp.route('/events/<int:id>', methods=['GET'])
def event_detail(id):
    """
    HTTP GET: /events/<id>
    顯示單一活動詳情與報名表單。
    呼叫 EventModel.get_by_id(id) 取得活動與報名人數狀態，
    若有效則渲染 detail.html，否則回傳 404 或重導向。
    """
    pass

@main_bp.route('/events/<int:id>/register', methods=['POST'])
def register_event(id):
    """
    HTTP POST: /events/<id>/register
    處理報名表單提交。
    取得報名者資料，呼叫 RegistrationModel.create(id, ...) 嘗試寫入資料。
    會利用 Model 內的交易機制處理報名邏輯及防超賣，若成功 flash 成功訊息，若捕捉到滿額例外則 flash 錯誤訊息，
    最後重導回原活動頁面。
    """
    pass
