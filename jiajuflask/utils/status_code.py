
OK = 200
SUCCESS = {'code': 200, 'msg': '请求成功'}
DATABASE_ERROR = {'code': 0, 'msg':'数据库错误，请稍后重试'}

#用户模块

USER_REGISTER_DATA_NOT_NULL = {'code': '1001', 'nsg':'请填写完整参数'}
USER_REGISTER_MOBILE_ERROR = {'code':'1002','msg': '手机号不正确'}
USER_REGISTER_PASSWORD_NOT_VALID = {'code': '1003', 'msg': '密码不正确'}
USER_REGISTER_MPBILE_EXSITS = {'code': '1004', 'msg': '该用户已存在'}

USER_LOGIN_USER_NOT_EXSITS = {'code': '1005', 'msg': '用户未注册，请注册'}
USER_LOGIN_USER_NOT_VALOD = {'code': '1006', 'msg': '密码不正确，请重新输入'}

USER_CHANGE_PROFILE_IMAGES = {'code': '1007', 'msg': '上传图片格式不正确'}


USER_CHANGE_PROFILE_IS_INVALID = {'code': '1008','msg': '用户名已存在'}


USER_AUTH_DATA_IS_NOT_NULL = {'code': '1009', 'msg': '实名认证请填写完整'}

USER_AUTH_ID_CARD_IS_NOT_VALID = {'code': '1010', 'msg': '身份证不匹配'}