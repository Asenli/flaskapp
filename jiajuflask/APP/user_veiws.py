import os
import re

from flask import Blueprint, render_template, request, url_for, redirect, session
from flask.json import jsonify


from APP.models import db, User
from utils import status_code


from utils.setting import UPLOAD_DIR
from utils.decoration import is_login

user_blueprint = Blueprint('user', __name__)


@user_blueprint.route('/')
def hello():
    return 'hello world'


@user_blueprint.route('/create_db/')
def create_db():
    db.create_all()
    return '创建成功'


@user_blueprint.route('/register/', methods=['GET'])
def user_register():
    if request.method == 'GET':
        return render_template('register.html')


##get 和post分开
@user_blueprint.route('/register/', methods=['POST'])
def register():
    """注册"""
    if request.method == 'POST':
        phone = request.form.get('mobile')
        pwd = request.form.get('password')
        password2 = request.form.get('passwd2')

        #验证完整性
        if not all([phone, pwd, password2]):
            return jsonify(status_code.USER_REGISTER_DATA_NOT_NULL)

        #验证手机正确性
        if not re.match(r'1[34578]\d{9}$', phone):
            return jsonify(status_code.USER_REGISTER_MOBILE_ERROR)
        #验证密码
        if pwd != password2:
            return jsonify(status_code.USER_REGISTER_PASSWORD_NOT_VALID)

        #4.保存数据
        user = User.query.filter(User.phone == phone).first()
        if user:
            return jsonify(status_code.USER_REGISTER_MPBILE_EXSITS)

        else:
            user = User()
            user.phone = phone
            user.password = pwd
            user.name = phone
            user.add_update()
            return jsonify(status_code.SUCCESS)


@user_blueprint.route('/login/', methods=['GET'])
def login():
    """登录"""
    return render_template('login.html')


@user_blueprint.route('/login/', methods=['POST'])
def user_login():
    """登录"""

    mobile = request.form.get('mobile')
    pwd = request.form.get('password')

    #1.验证数据完整性
    if not all([mobile, pwd]):
        return jsonify(status_code.USER_REGISTER_DATA_NOT_NULL)

    #2.验证手机正确性
    if not re.match(r'1[34578]\d{9}$', mobile):
        return jsonify(status_code.USER_REGISTER_MOBILE_ERROR)

    #3.验证用户 第一个用户,返回用户实例
    user = User.query.filter(User.phone == mobile).first()
    if user:
        #校验密码
        if not user.check_pwd(pwd):
            return jsonify(status_code.USER_LOGIN_USER_NOT_VALOD)

        #4.验证用户成功
        session['user_id'] = user.id
        return jsonify(status_code.SUCCESS)
    else:
        return jsonify(status_code.USER_LOGIN_USER_NOT_EXSITS)


@user_blueprint.route('/my/', methods=['GET'])
@is_login
def my():
    """个人中心首页"""

    return render_template('my.html')


@user_blueprint.route('/profile/', methods=['GET'])
def profile():
    """头像上传"""
    return render_template('profile.html')


#上传文件时用patch
@user_blueprint.route('/profile/', methods=['PATCH'])
@is_login
def user_profile():
    file = request.files.get('avatar')
    #校验上传图片格式的正确性
    if not re.match(r'image/.*', file.mimetype):
        return jsonify(status_code.USER_CHANGE_PROFILE_IMAGES)
    #保存
    image_path = os.path.join(UPLOAD_DIR, file.filename)
    file.save(image_path)

    user = User.query.get(session['user_id'])
    avatar_path = os.path.join('upload', file.filename)
    #头像保存路径，后面ajax会需要拿这个路径
    user.avatar = avatar_path

    try:
        user.add_update()
    except Exception as e:

        return jsonify(status_code.DATABASE_ERROR)

    return jsonify(code=status_code.OK, image_path=avatar_path)


@user_blueprint.route('/proname/', methods=['PATCH'])
@is_login
def user_proname():
    #获取用户名
    name = request.form.get('name')
    #获取到页面里面name 和数据库name对应
    user = User.query.filter_by(name=name).first()
    if user:
        #过滤用户名是否存在
        return jsonify(status_code.USER_CHANGE_PROFILE_IS_INVALID)

    else:
        user = User.query.get(session['user_id'])
        #修改name值
        user.name = name
        try:
            user.add_update()
        except:
            db.session.rollback()
            return jsonify(status_code.DATABASE_ERROR)
        return jsonify(code=status_code.OK, name=name)


@user_blueprint.route('/logout/', methods=['GET'])
@is_login
def user_logout():
    """用户退出"""
    session.clear()
    return redirect(url_for('user.login'))


@user_blueprint.route('/user/', methods=['GET'])
@is_login
def user_info():
    """用户个人信息拿取"""
    user = User.query.get(session['user_id'])

    return jsonify(code=status_code.OK, data=user.to_basic_dict())


@user_blueprint.route('/auth/', methods=['GET'])
def auth():
    return render_template('auth.html')


@user_blueprint.route('/auth/', methods=['PATCH'])
def user_auth():
    """
    身份证认证
    :return:
    """
    real_name = request.form.get('real_name')
    id_card = request.form.get('id_card')

    if not all([real_name, id_card]):
        return jsonify(status_code.USER_AUTH_DATA_IS_NOT_NULL)

    if not re.match(r'^[1-9]\d{17}$', id_card):
        return jsonify(status_code.USER_AUTH_ID_CARD_IS_NOT_VALID)

    user = User.query.get(session['user_id'])
    user.id_name = real_name
    user.id_card = id_card
    try:
        user.add_update()
    except:
        db.session.rollback()
        return jsonify(status_code.DATABASE_ERROR)
    return jsonify(status_code.SUCCESS)


@user_blueprint.route('/auths/', methods=['GET'])
@is_login
def user_auths():
    """实名认证信息拿取"""
    user = User.query.get(session['user_id'])
    return jsonify(code=status_code.OK, data=user.to_auth_dict())

