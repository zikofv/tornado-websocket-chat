import tornado.ioloop
import tornado.web
import tornado.websocket
import json
from js_operations import js_ops

class ClientManager(object):
  def __init__(self):
    self.clients = set()

  def get_clients(self):
    return self.clients

  def add_client(self, client):
    self.clients.add(client)

  def remove_client(self, client):
    self.clients.remove(client)

class MainHandler(tornado.web.RequestHandler):
  def initialize(self, js_ops_names):
    self.js_ops_names = js_ops_names

  def get(self):
    self.render("index.html", js_ops_names=self.js_ops_names)

class CommunicationWebSocket(tornado.websocket.WebSocketHandler):

  def initialize(self, mmanager, js_ops):
    self.mmanager = mmanager
    self.js_ops = js_ops

  def open(self):
    self.mmanager.add_client(self)
    print "WebSocket opened"

  def on_message(self, message):
    msg = json.loads(message)

    if msg["operation"] == "chat":
      for i in self.mmanager.get_clients():
        i.write_message(json.dumps({"operation" : "chat", "chat" : msg["chat"]}))

    elif msg["operation"] == "js_op":
      op_number = int(msg["operation_index"])
      if 0 <= op_number < len(self.js_ops):
        js_object = self.js_ops[op_number]
        for i in self.mmanager.get_clients():
          i.write_message(json.dumps(js_object))

  def on_close(self):
    self.mmanager.remove_client(self)
    print "WebSocket closed"

manager = ClientManager()

application = tornado.web.Application([
  (r"/", MainHandler, {"js_ops_names" : [(i, j["name"]) for i,j in enumerate(js_ops)]}),
  (r'/ws', CommunicationWebSocket, {"mmanager" : manager, "js_ops" : js_ops}),
  (r'/static/(.*)', tornado.web.StaticFileHandler, {'path': "."}),
])

if __name__ == "__main__":
  application.listen(8888)
  tornado.ioloop.IOLoop.instance().start()
