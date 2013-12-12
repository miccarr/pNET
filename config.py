#!/usr/bin/env python
# pNET - Citizen network ====================================================
# Free to share, edit, copy this code, but you must crediting pNET as source.
# pBOX CONFIGURATION FILE

config={}

# Wireless interface names =================================
config['if', 'parent'] = 'wlan0'
config['if', 'childs'] = 'wlan1'

# Node & domain infos ======================================
config['node', 'name'] = "first" # .node.pnet
config['node', 'domain'] = "" # .pnet
config['node', 'delegate'] = "" # delegate domain to another
config['node', 'desc'] = "" # Describe your domain
config['node', 'keywords'] = [] # Keywords for your domain