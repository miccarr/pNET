#!/usr/bin/env python
# -*- coding: utf-8 -*- 
# pNET - Citizen network ====================================================
# Free to share, edit, copy this code, but you must crediting pNET as source.
# pBOX CONFIGURATION FILE

conf={}

# Wireless interface names =================================
conf['if', 'parent'] = 'wlan0'
conf['if', 'childs'] = 'wlan1'

# Node & domain infos ======================================
conf['node', 'name'] = "first" # .node.pnet
conf['node', 'domain'] = "" # .pnet
conf['node', 'delegate'] = "" # delegate domain to another
conf['node', 'desc'] = "" # Describe your domain
conf['node', 'keywords'] = [] # Keywords for your domain

# Files sharing ============================================
conf['files', 'dir'] = "/root/files.pnet/"
