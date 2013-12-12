#!/usr/bin/env python
# pNET - Citizen network ====================================================
# Free to share, edit, copy this code, but you must crediting pNET as source.
# pINIT defines the node ID, configure and start DHCP server

import urllib
import urllib2
import commands
import config

cmd = commands.getoutput

cmd('ifconfig ' + config['if','childs'] +' up')
childsMAC = cmd("ifconfig " + config['if','childs'] + " | grep -o -E '([[:xdigit:]]{1,2}:){5}[[:xdigit:]]{1,2}'")
cmd('ifconfig ' + config['if','childs'] +' down')

# Selecting node id
nodeID = ''
while nodeID == '':
	# Updating node list from parent node
	print "[pNET] pINIT : Updating list of nodes"
	cmd('rm /etc/resolv.conf')
	urllib.urlretrieve('http://parent.pnode/nodes','/etc/resolv.conf')

	# Matching first unused id
	f = open('/etc/resolv.conf', 'r')
	nodes = f.readlines()[11:]
	f.close()

	myid = ''
	i = 0
	while i <= 255:
		j = 0
		while j <= 255:
			if not( i+j==0 or i+j==2*255):
				if not('10.'+str(i)+'.'+str(j)+'.254' in nodes):
					myid = str(i)+'.'+str(j)
					i = 256
					j = 256
			j += 1
		i += 1

	print "[pNET] pINIT : Using '"+myid+"' -> ",
	valid = urllib2.urlopen('http://parent.node/register/'+myid).read()
	if valid == 'ok':
		print "<OK>"
		nodeID = myid
	else:
		print "<USED>"

# DHCP Configuration
f = open('/etc/dhcpd.conf', 'w')
f.write("ddns-update-style ad-hoc;\n")
f.write("ignore client-updates;\n")
f.write("subnet 10."+nodeID+".0 netmask 255.255.255.0 {\n")
f.write("    range 10."+nodeID+".1 10."+nodeID+".250;\n")
f.write("    option subnet-mask 255.255.255.0;\n")
f.write("    option broadcast-adress 10."+nodeID+".255;\n")
f.write("}\n")
f.write("option routers 10."+nodeID+".254;\n")
f.write("option domain-name 'node.pnet';\n")
f.write("option domain-name-servers ")
ns = "10."+nodeID+".254\n" #current node first
ns += cmd("cat /etc/resolv.conf|grep 'nameserver'|awk '{print $2}'")
ns = ns.split('\n')
print ', '.join(ns)
f.write(";\n")
f.write("option ipforwarding off;\n")
f.write("default-lease-time 14400;\n")
f.write("max-lease-time 43200;\n")
f.write("host node{\n")
f.write("    hardware ethernet "+childsMAC+"\n")
f.write("    fixed-address 10."+nodeID".254\n")
f.write("    option host-name '"+childsMAC.replace(':','')+".node.pnet';\n")
f.write("}\n")

#f.write("    on commit {\n")
#f.write("        set ClientIP = binary-to-ascii(10, 8, '.', leased-address);\n")
#f.write("        set ClientMac = binary-to-ascii(16, 8, ':', substring(hardware, 1, 6));\n")
#f.write("        execute('/usr/sbin/my_script_here', 'commit', ClientIP, ClientMac);\n")
#f.write("    }\n")
f.close()
f = open('/etc/conf.d/dhcp', 'w')
f.write('DHCP4_ARGS="-q ' + config['if','childs'] + '"')

# Starting up DHCPd
cmd('systemctl restart dhcpd.service')