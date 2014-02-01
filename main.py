from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from server import app
from sqlalchemy import create_engine
from model.model import Session, Base

engine = create_engine('postgresql://postres:@localhost/scheduleDB')
Session.configure(bind = engine)

Base.metadata.create_all(engine)

http_server = HTTPServer(WSGIContainer(app))
http_server.listen(80)
IOLoop.instance().start()
