import tornado.httpserver
import tornado.ioloop
import tornado.web
import sys
import asyncio
import settings
import queue

from concurrent.futures import ThreadPoolExecutor
from app.stock.handlers.stock_handlers import DataInsertHandler, AjaxStockPriceHandler, WSHandler
from app.accounts.handlers.signup_handler import SignUpHandler
from app.accounts.handlers.login_handler import LoginHandler, LogoutHandler
from app.stock.controller.stock_price_crawler_agent import ThreadAgentsManager


if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    # The default has changed from selector to pro-actor in Python 3.8.
    # Thus, this line should be added to detour probable errors


if __name__ == "__main__":
    executor = ThreadPoolExecutor(max_workers=4)
    thread_agent_manager_queue = queue.Queue()

    settings = {"template_path": settings.TEMPLATE_PATH,
                "static_path": settings.STATIC_PATH,
                "cookie_secret": "fAZRXY664jE6ke9ww1IosKYmdaqocecPg0GygPd3qhOwfvVHYy52YdorlV+oFZCOhtU=",
                "login_url": "/login"
                }

    application = tornado.web.Application([
        (r"/login", LoginHandler),
        (r"/input-stock-code", DataInsertHandler),
        (r"/ws", WSHandler, dict(queue=thread_agent_manager_queue)),
        (r"/show-all", AjaxStockPriceHandler, dict(executor=executor)),
        (r"/logout", LogoutHandler),
        (r"/sign-up", SignUpHandler)
    ], **settings)

    http_server = tornado.httpserver.HTTPServer(application)

    socket_address = 8888
    http_server.listen(socket_address)

    thread_agent_manager = ThreadAgentsManager(thread_agent_manager_queue)
    thread_agent_manager.start()

    loop = tornado.ioloop.IOLoop.current()
    loop.start()

    thread_agent_manager.stop()
