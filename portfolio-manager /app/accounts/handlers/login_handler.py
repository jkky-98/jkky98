import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.escape
import json

from app.accounts.models import user_model
from app.accounts.models.user_model import User


class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return User.from_request(self)


class LoginHandler(BaseHandler):
    def __init__(self, application, request):
        super(LoginHandler, self).__init__(application, request)

    def set_current_user(self, user_name):
        if user_name:
            self.set_secure_cookie("user", user_name)
        else:
            self.clear_cookie("user")

    def check_permission(self, user_name, user_password):
        # return User() class object
        user = user_model.get_user(user_name, user_password)
        if user:
            self.set_secure_cookie("user_id", user.user_id)
            return True
        return False

    def post(self):
        user_data = tornado.escape.json_decode(self.request.body)
        user_name = user_data.get('user_name', None)
        user_password = user_data.get('user_password', None)
        auth = self.check_permission(user_name, user_password)

        if auth:
            self.set_current_user(user_name)
            self.write(json.dumps({'success': True, 'error_msg': '', 'current_user_name': user_name}))
        else:
            self.write(json.dumps({'success': False, 'error_msg': 'Wrong ID or Password', 'current_user_name': ''}))


class LogoutHandler(BaseHandler):
    def get(self):
        if self.current_user:
            self.write({'success': False, 'error_msg': 'Logout Failed'})
        else:
            self.write({'success': True, 'error_msg': ''})
