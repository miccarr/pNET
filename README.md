pNET
====
Sketchy citizen wireless network for RPi

Files
-----
- **config.py**     Configuration files
- **pDISCOVER.py**  Watch around networks to select a pNET parent and connect to it
- **pINIT.py**      Defines the node ID, configure and start DHCP server
- **pHOME.py**      Web interface and HTTP API to organize nodes
- **pDNS.py**		Peer to peer DNS resolver / Domain Name conflict resolver
- **d4ec20a0c5eb7be376176804d1fd528a.info**		File info sample

Disambiguation
--------------
###DNS
- **node.pnet.**		Name of the current node.
- **parent.pnet.**	Name of the parent of the current node.
- **<MAC ADRESS>.mac.pnet.** Redirection to the last known IP of the mac adress.
- **file.pnet.**		Alias for node.pnet, file upload interface.
- ***\<MD5\>*.file.pnet.** Info about the file.
- ***\<PART\>*.*\<MD5\>*.file.pnet.** Redirection to the first file part owner.
- **home.**			Alias for node.pnet, main portal.
- **node.**			Alias for node.pnet, main portal.

###HTTP API
- **node.pnet/** (HTML) Main portal
- **node.pnet/files** (XML) List of known md5 files with title, keyword, desc.,...
- **node.pnet/nodes** List of known nodes IP
- **node.pnet/childs** List of childs nodes
- **node.pnet/search?q=*\<KEYWORD\>*** (HTML) Search <KEYWORD> related files / website
- **search.node.pnet/*\<KEYWORD\>*** (XML) Search <KEYWORD> related files / website
- **\*/search/*\<KEYWORD\>*** (XML) Search <KEYWORD> related files / website on this node
- **file.pnet/<MD5>** Download MD5 related file
