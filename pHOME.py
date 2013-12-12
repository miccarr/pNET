#!/usr/bin/env python

from BaseHTTPServer import HTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler

class HTTPHandler (SimpleHTTPRequestHandler):
	server_version = "pHOME-for-pNET/HTTP/0.1"
	
	def do_GET(self):
		if(self.path[0:4] == "/new" && self.client_address[0:-3]=='10.0.0.'):
			self.send_response(200, 'OK')
			self.end_headers()
			self.wfile.write("0.5")
		elif(self.path[0:4] == "/iam"):
			self.send_response(200, 'OK')
			self.end_headers()
			self.wfile.write("saved")
		else:
			if(self.headers["host"] == "node.pnet"):
				self.send_response(200, 'OK')
				self.send_header('Content-type', 'text/html')
				self.end_headers()
				self.wfile.write("<html><head><title>pNET .:HOME:.</title></head><body><h1>pNET</h1><small>The citizen network</small></body></html>")
			elif(self.headers["host"][-4] == ".pnet"):
				self.send_response(300, 'Multiple Choices')
				self.send_header('Content-type', 'text/html')
				self.end_headers()
				self.wfile.write("<html><head><title>pNET .:DNS RESOLVE:.</title></head><body>")
				self.wfile.write("<h1>'" + self.headers["host"] + "'</h1><ul>")
				self.wfile.write('<li><a href="B8E8562ED536.mac.pnet">B8E8562ED536.mac.pnet</a> (10.0.38.254) <i>no description</i></li>')
				self.wfile.write('<li><a href="BAE856E26B00.mac.pnet">BAE856E26B00.mac.pnet</a> (10.0.15.254) <i>Yolo</i></li>')
				self.wfile.write("</ul></body></html>")
			else:
				self.send_response(200, 'OK')
				self.end_headers()
				self.wfile.write("parents{'0.1'}\nchilds{'0.3','0.4'}")
			

try:
	httpd = HTTPServer(('', 80), HTTPHandler)
	print "[pNET] pHOME : started"
	httpd.serve_forever()

except KeyboardInterrupt:
	print "[pNET] pHOME : ended by ^C"

except Exception, error:
	print "[pNET] pHOME error: " + str(error)
	sys.exit()