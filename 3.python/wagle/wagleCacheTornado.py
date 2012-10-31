#!/usr/bin/env python
#
# Copyright 2009 Facebook
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options

import sys

import wagleCacheServer
import logging

define("port", default=8888, help="run on the given port", type=int)


class MainHandler(tornado.web.RequestHandler):
    def get(self):
	#print self.request
	#print self.request.path
	
	#print "FROM client: ", self.path
	paras = self.request.path
	paras = unicode(paras, 'ascii')
	paras = paras.encode('utf-8')

	flds = paras.split('/')
	flds = filter(len, flds) # get the list of a string which is not empty. len(x) > 0
	uid = flds[1]

	logger.debug('REQ: %s' % ','.join(flds))

	res = ''
	if flds[0] == "timeline":
		res = waglecache.timeline(uid)
	elif flds[0] == "login":
		res = waglecache.login(uid)
	elif flds[0] == "post":
		res = waglecache.post(uid, flds[2])
	elif flds[0] == "follow":
		res = waglecache.follow(uid, flds[2])
	elif flds[0] == "unfollow":
		res = waglecache.unfollow(uid, flds[2])
	else:
		
		return

        self.write(res)


def main():
    tornado.options.parse_command_line()
    application = tornado.web.Application([
        (r"/.*", MainHandler),
    ])
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
	global waglecache

	logger = logging.getLogger('wagletornado')
	hdlr = logging.FileHandler('./wagletornado.log')
	formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
	hdlr.setFormatter(formatter)
	logger.addHandler(hdlr)
	logger.setLevel(logging.INFO)
	logger.info('==== starts: %s' % ' '.join(sys.argv))


	## load DB first
	## 211.233.77.6 = wagle 1st db
	## 211.233.77.7 = wagle 2nd db
	dbhandler = wagleCacheServer.WagleDB('211.233.77.7')
	waglecache = wagleCacheServer.WagleCache(dbhandler, logger)
	waglecache.add_contents_list()
	waglecache.add_friends_list()

	main()
