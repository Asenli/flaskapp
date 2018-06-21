from functools import wraps

from flask import session, redirect, url_for


def is_login(func):
    """
    装饰器用于登录验证
    :param func:
    :return:
    """
    @wraps(func)
    def check_login(*args, **kwargs):
        #验证session里面有没有用户id名

        if 'user_id' in session:
            return func(*args, **kwargs)
        else:

            return redirect(url_for('user.login'))
    return check_login
