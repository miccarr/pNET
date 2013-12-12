#!/usr/bin/env python

import socket
import urllib2
import commands
import config

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
  
  def searchFor(self, fqdn):
  	cIP = cmd("ifconfig "+config['if','childs']+" | grep inet | awk ‘{print $2}’ | sed ‘s/addr://’ | grep .")
  	cMAC = cmd("ifconfig " + config['if','childs'] + " | grep -o -E '([[:xdigit:]]{1,2}:){5}[[:xdigit:]]{1,2}'")
	if(fqdn in ["node.pnet.", cMAC.replace(':','')+".mac.pnet.", ".pnet.", config['node', 'name']+".node.pnet", ]):
		return cIP
	elif(config['node','domain']!='' and fqdn == config['node','domain']+'.pnode.'):
		if(config['node','delegate']!=''):
			return config['node','delegate']
		else:
			return cIP
	return '';
  
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
  
  try:
    while 1:
      data, addr = udps.recvfrom(1024)
      p=DNSQuery(data)
      ip = p.searchFor(p.domaine)
      if ip != '':
      	udps.sendto(p.reponse(ip), addr)
      	print '[pNET] pNS: %s -> %s' % (p.domaine, ip)
  except KeyboardInterrupt:
    print '[pNET] pNS: HALTED WITH ^C'
    udps.close()