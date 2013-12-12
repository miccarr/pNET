#!/usr/bin/env python
# pNET - Citizen network ====================================================
# Free to share, edit, copy this code, but you must crediting pNET as source.
# pDISCOVER watch around networks to connect them


import config
import commands
import re

cmd = commands.getoutput

# Starting up PARENT interface
print "[pNET] pDISCOVER : Starting up parent interface"
cmd('ifconfig ' + config['if','parent'] +' down')
cmd('ifconfig ' + config['if','parent'] +' up')

# Watching for other pNET box by scanning SSIDs
print "[pNET] pDISCOVER : Scanning reachable pNET : ",
stdout = cmd('iwlist ' + config['if','parent'] + ' scan')
stdout = stdout.split('\n')
ssid_list = []
for line in stdout:
	line = line.strip()
	match = re.search('ESSID:"(\S+)"',line)
	if match:
		if (match.group(1)[0:5] == "pNET-"):
        	ssid_list.append(match.group(1))
        	print "+", # IT'S A pNET ! SAVE IT
    	else:
    		print "-", # DON'T CARE ABOUT OTHERS NETWORKS
print "\n[pNET] pDISCOVER : Found " + len(essid) + " pBOX around you"

# Search and integrate the biggest pNET
if len(ssid_list) != 0:
	if len(ssid_list) > 1:
		ssid_list.sort()
		pNET = {}
		for ssid in ssid_list:
			cmd('iwconfig  ' + config['if','parent'] + ' essid "' + ssid + '"')
			cmd('dhclient ' + config['if','parent'])
			ns = cmd("cat /etc/resolv.conf|grep 'nameserver'")
			ns.split('\n')
			size[len(ns)] = ssid
			cmd("rm /etc/resolv.conf && dhclient " + config['if','parent'] + " -r")
		ssid = d[max(d)]
		print "\n[pNET] pDISCOVER : Biggest pNET via '" + ssid + "' (" + max(d) +" pNODES)"
	elif len(ssid_list) == 1:
		ssid = ssid_list[0]
		print "\n[pNET] pDISCOVER : Biggest pNET via '" + ssid + "' (Unique)"
	cmd('iwconfig  ' + config['if','parent'] + ' essid "' + ssid + '"')
	cmd('dhclient ' + config['if','parent'])
	
	# Define parent.pNET and node.pNET
	#myIP = cmd('ifconfig ' + config['if','parent'] + "|grep 'inet '|awk '{print $2}'")
	parent = cmd('netstat -rn|grep ' + config['if','parent'] + "|grep '0.0.0.0'|awk '{print $3}'")
	f = open('/etc/hosts','w')
	f.write('127.0.0.1 localhost\n')
	f.write(parent + ' parent.pnet\n')
	f.close()
else:
	cmd('ifconfig ' + config['if','parent'] +' down')
	print "\n[pNET] pDISCOVER : You are a pioneer..."
	f = open('/etc/hosts','w')
	f.write('127.0.0.1 localhost\n')
	f.write('127.0.0.1 parent.pnet\n')
	f.close()