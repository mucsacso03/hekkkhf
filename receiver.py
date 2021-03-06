#!/usr/bin/env python3
# receiver.py

import os, sys, getopt, time
from netinterface import network_interface
# from client import c_incoming
import server
import client
from common_code import net_path

NET_PATH = net_path() # 'C:/Users/David/PycharmProjects/client'
OWN_ADDR = ''

# ------------       
# main program
# ------------

try:
    opts, args = getopt.getopt(sys.argv[1:], shortopts='hp:a:', longopts=['help', 'path=', 'addr='])
except getopt.GetoptError:
    print('Usage: python receiver.py -p <network path> -a <own addr>')
    sys.exit(1)

for opt, arg in opts:
    if opt == '-h' or opt == '--help':
        print('Usage: python receiver.py -p <network path> -a <own addr>')
        sys.exit(0)
    elif opt == '-p' or opt == '--path':
        NET_PATH = arg
    elif opt == '-a' or opt == '--addr':
        OWN_ADDR = arg

if (NET_PATH[-1] != '/') and (NET_PATH[-1] != '\\'): NET_PATH += '/'

if not os.access(NET_PATH, os.F_OK):
    print('Error: Cannot access path ' + NET_PATH)
    sys.exit(1)

if len(OWN_ADDR) > 1: OWN_ADDR = OWN_ADDR[0]

if OWN_ADDR not in network_interface.addr_space:
    print('Error: Invalid address ' + OWN_ADDR)
    sys.exit(1)

# main loop
netif = network_interface(NET_PATH, OWN_ADDR)
print('Receiver started...')
while True:
    # Calling receive_msg() in non-blocking mode ...
    #	status, msg = netif.receive_msg(blocking=False)
    #	if status: print(msg)      # if status is True, then a message was returned in msg
    #	else: time.sleep(2)        # otherwise msg is empty

    # Calling receive_msg() in blocking mode ...
    status, msg = netif.receive_msg(blocking=True)  # when returns, status is True and msg contains a message
    if OWN_ADDR == 'S':
        # server = Server(input('Give me the passphrase for decrypting server key: '))
        # print('Server incoming')
        server.s_incoming(msg)

        # server.s_incoming(msg)
    if OWN_ADDR == 'C':
        # print('Client incoming')
        client.c_incoming(msg)
        # client.c_incoming(msg)
    # print(msg.decode('utf-8'))
