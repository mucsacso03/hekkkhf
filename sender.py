#!/usr/bin/env python3
#sender.py

import os, sys, getopt, time
from netinterface import network_interface
from common_code import net_path

NET_PATH = net_path() #'C:/Users/David/PycharmProjects/client'
OWN_ADDR = ''
MSG = 'default'
DST = ''
# ------------       
# main program
# ------------

try:
	opts, args = getopt.getopt(sys.argv[1:], shortopts='hp:a:d:m:', longopts=['help', 'path=', 'addr=', 'dst=', 'msg='])
except getopt.GetoptError:
	print('Usage: python sender.py -p <network path> -a <own addr>')
	sys.exit(1)

for opt, arg in opts:
	if opt == '-h' or opt == '--help':
		print('Usage: python sender.py -p <network path> -a <own addr>')
		sys.exit(0)
	elif opt == '-p' or opt == '--path':
		NET_PATH = arg
	elif opt == '-a' or opt == '--addr':
		OWN_ADDR = arg
	elif opt == '-d' or opt == '--dst':
		DST = arg
	elif opt == '-m' or opt == '--msg':
		MSG = arg


if (NET_PATH[-1] != '/') and (NET_PATH[-1] != '\\'): NET_PATH += '/'

if not os.access(NET_PATH, os.F_OK):
	print('Error: Cannot access path ' + NET_PATH)
	sys.exit(1)

if len(OWN_ADDR) > 1: OWN_ADDR = OWN_ADDR[0]

if OWN_ADDR not in network_interface.addr_space:
	print('Error: Invalid address ' + OWN_ADDR)
	sys.exit(1)

# main loop


def send_faszom(msg, own_addr, dst):
	OWN_ADDR = own_addr
	netif = network_interface(NET_PATH, OWN_ADDR)
	netif.send_msg(dst, msg)

# #print('Main loop started...')
# while True:
# 	if DST == '' or OWN_ADDR == '':
# 		print('Error - missing values: DST or OWN_ADDR')
# 		break
# 	#netif.send_msg(DST, MSG.encode('utf-8'))
# 	break
# 	#if input('Continue? (y/n): ') == 'n': break
