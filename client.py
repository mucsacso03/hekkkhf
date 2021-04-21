import os
import threading

from netinterface import network_interface
from common_code import send_message, make_message, net_path  # , receiver_thread

commands = ['LGN', 'LGO', 'MKD', 'RMD', 'RMF', 'GWD', 'CWD', 'LST', 'UPL', 'DNL']

NET_PATH = net_path() #'C:/Users/David/PycharmProjects/client'
OWN_ADDR = 'C'


def receiver_t():
    os.system('python C:/Users/David/PycharmProjects/client/receiver.py --addr ' + OWN_ADDR)


def valid_command(command):
    for x in commands:
        if command.upper() == x:
            # Ha talál egyezést akkor false-t küldd vissza, hogy ne fusson le a hibaüzenet
            return False

    return True


def command_line():
    while True:
        message = ''
        command = input()
        command_array = command.split()
        if command == '' or valid_command(command_array[0]):  # hibát dob ha nem létező parancsot ad meg a user
            print('Wrong command')

        elif command_array[0].upper() == commands[0]:  # LGN
            pass
            # TODO

        elif command_array[0].upper() == commands[1]:  # LGO
            pass
            # TODO

        elif command_array[0].upper() == commands[2]:  # MKD
            if len(command_array) == 2:  # ha kettő hosszú akkor van benne egy paraméter.
                message = make_message(command_array)
                send_message(OWN_ADDR, 'S', message)
            else:
                print("Error - bad parameter")

        elif command_array[0].upper() == commands[8]: # UPL
            if len(command_array) == 2:  # ha kettő hosszú akkor van benne egy paraméter.
                in_file = open(command_array[1], "rb")  # opening for [r]eading as [b]inary
                data = in_file.read()
                in_file.close()
                message = 'upl' + os.path.basename(in_file.name) + make_message(data.decode('utf-8')) # just for demonstration
                send_message(OWN_ADDR, 'S', message)
            else:
                print("Error - bad parameter")

        else:
            message = make_message(command_array)
            send_message(OWN_ADDR, 'S', message)


def c_incoming(msg):
    print('Incoming message: ' + str(msg,'utf-8'))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    x = threading.Thread(target=receiver_t)
    x.start()
    command_line()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
