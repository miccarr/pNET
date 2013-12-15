#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import socket
import urllib2
import commands
from config import *

cmd = commands.getoutput

class DNSQuery:
  def __init__(self, data):
    self.data=data
    self.domaine=''

    type = (ord(data[2]) >> 3) & 15   # Opcode bits
    if type == 0:                     # Standard query
      ini=12
      lon=ord(data[ini])
      while lon != 0:
        self.domaine+=data[ini+1:ini+lon+1]+'.'
        ini+=lon+1
        lon=ord(data[ini])
  
  def resolve1(self,conf):
  	cIP = cmd("ifconfig "+conf['if','childs']+" | grep inet | awk '{print $2}' | sed 's/addr://' | grep '10.'")
  	cMAC = cmd("ifconfig " + conf['if','childs'] + " | grep -o -E '([[:xdigit:]]{1,2}:){5}[[:xdigit:]]{1,2}'")
	cMAC = cMAC.replace(':','')
	if self.domaine in ["node.pnet.", cMAC+".mac.pnet.", conf['node','name']+".node.pnet"]:
		return cIP
	elif(self.domaine == conf['node','domain']+'.pnode.'):
		if(conf['node','delegate']!=''):
			return conf['node','delegate']
		else:
			return cIP
	elif(self.domaine == 'file.pnet.'):
		return cIP
	elif(self.domaine[-10:] == 'file.pnet.'):
		file=self.domaine.split('.')
		if(len(file)==5):
			if(is_file(conf['files','dir']+'/'+file[1]+'.part'+file[0])):
				return cIP
		elif(len(file)==4):
			if(is_file(conf['files','dir']+'/'+file[0]+'.info')):
				return cIP
	return ''
  
  def reponse(self, ip):
	packet=''
	if self.domaine[-6:]==".pnet.":
		packet+=self.data[:2] + "\x81\x80"
		packet+=self.data[4:6] + self.data[4:6] + '\x00\x00\x00\x00'   # Questions and Answers Counts
		packet+=self.data[12:]                                         # Original Domain Name Question
		packet+='\xc0\x0c'                                             # Pointer to domain name
		packet+='\x00\x01\x00\x01\x00\x00\x00\x3c\x00\x04'             # Response type, ttl and resource data length -> 4 bytes
		packet+=str.join('',map(lambda x: chr(int(x)), ip.split('.'))) # 4bytes of IP
	return packet

if __name__ == '__main__':

  udps = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  udps.bind(('',53))
  
  print '[pNET] pNS: Started'
  
  try:
    while 1:
      data, addr = udps.recvfrom(1024)
      p=DNSQuery(data)
      ip = p.resolve1(conf)
      if ip != '':
      	udps.sendto(p.reponse(ip), addr)
      	print '[pNET] pNS: responded "%s" -> %s' % (p.domaine, ip)
      elif(p.domaine[-6:]=='.pnet.'):
      	print '[pNET] pNS: unknown "%s"' % (p.domaine)
  except KeyboardInterrupt:
    print "\n[pNET] pNS: HALTED WITH ^C"
    udps.close()