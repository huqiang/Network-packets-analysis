Programming Assignment 2
CS3103 Sem1 AY1213
Hu Qiang
A0077857J


###########
#IMPORTANT#
###########
This program is written in Python3, and it does not support Python 2
due to the change of built-in libraries (bytes.fromhex()) and I am
lazy to make it compatible with Python 2

1, Developement Environment:
	OS: Mac OS X 10.8.2 Mountain Lion
	Python: 3.3.0

2, Running option:
	python3 program input_file [output_file]
	For example: python3 dns.py hex.dat dnsout.txt will display the result
	on terminal and write to dnsout.txt

3, Sample outputs for analysing hex.dat are:
	countout.txt	for analysing number of different packets
	dnsout.txt	for analysing DNS A response
	dhcpout.txt	for analysing DHCP packets

4, Extra packets analysis:
	DHCP
	Since there are too many DHCP options(http://www.iana.org/assignments/bootp-dhcp-parameters/bootp-dhcp-parameters.xml) and I cannot implement all of them, so I just implemented which are used in hex.dat.

5, Both dns.py and dhcp.py are based on count.py, so it is easier to look through the code
of count.py to know the structure. 
Also the codes are not refactored, I am sorry about that.