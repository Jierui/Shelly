# -*- encoding:utf-8 -*-
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
from pyftpdlib.authorizers import DummyAuthorizer


class MyHandler(FTPHandler):

    def on_connect(self):
        print ("%s:%s connected" % (self.remote_ip, self.remote_port))

    def on_disconnect(self):
        # do something when client disconnects
        pass

    def on_login(self, username):
        # do something when user login
        pass

    def on_logout(self, username):
        # do something when user logs out
        pass

    def on_file_sent(self, file):
        # do something when a file has been sent
        print(self.username, file)
        pass

    def on_file_received(self, file):
        # do something when a file has been received
        print(self.username, file)
        pass

    def on_incomplete_file_sent(self, file):
        # do something when a file is partially sent
        print(self.username, file)
        pass

    def on_incomplete_file_received(self, file):
        # remove partially uploaded files
        import os
        os.remove(file)


def main():
    authorizer = DummyAuthorizer()
    authorizer.add_user('user', '12345', '/Users/jiehan/ndmcrio/data-ana/download', 'elradfmwMT')
    authorizer.add_anonymous('/Users/jiehan/ndmcrio/data-ana/download')

    handler = MyHandler
    handler.authorizer = authorizer
    server = FTPServer(('', 2121), handler)
    server.serve_forever()

'''
作者：gaoshine
链接：https://www.jianshu.com/p/7a63d0a210f2
'''

if __name__ == "__main__":
    main()

