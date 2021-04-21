import os
import threading

from netinterface import network_interface
from common_code import send_message, concat_str, net_path  # , receiver_thread

valid_commands = ['LGN', 'LGO', 'MKD', 'RMD', 'RMF', 'GWD', 'CWD', 'LST', 'UPL', 'DNL']
#                   0      1      2      3      4      5      6      7      8      9
NET_PATH = net_path()  # 'C:/Users/David/PycharmProjects/client'
OWN_ADDR = 'C'


def receiver_t():
    # Külön szálként indítva elindul a receiver
    os.system('python C:/Users/David/PycharmProjects/client/receiver.py --addr ' + OWN_ADDR)


def valid_command(command):
    valid_command_with_0_param = [valid_commands[1], valid_commands[5], valid_commands[7]]  # LGO, GWD, LST
    valid_command_with_1_param = [valid_commands[2], valid_commands[3], valid_commands[4],
                                  valid_commands[6]]  # MKD, RMD, RMF, CWD
    valid_command_with_2_param = [valid_commands[0], valid_commands[8], valid_commands[9]]  # LGN, UPL, DNL

    valid_command_with_x_param_array = [valid_command_with_0_param, valid_command_with_1_param,
                                        valid_command_with_2_param]
    expected_params_count = 0

    # paraméter helyes mennyiségének megvizsgálása. 0,1,2 counter érték esetén ha belépünk az if-be találat miatt akkor
    # összetudjuk hasonlítani a kapott paraméterek mennyiségét az elvártal.
    for y in valid_command_with_x_param_array:
        if any(x in command[0].upper() for x in y):
            if len(command) != expected_params_count + 1:
                print("Error - bad parameter")
                return True
            return False  # ha egyezik a paraméter szám az elvártal akkor az előző ifbe nem lép be és ezzel visszatérünk
        expected_params_count += 1

    print('Error - Wrong command')
    return True


def make_message(command, params):  # command = string, params = string array(len=0/1/2)
    # ---------demo-------------
    if command.upper() == valid_commands[8]:
        in_file = open(params[0], "rb")  # opening for [r]eading as [b]inary
        data = in_file.read()
        in_file.close()
        message = 'upl' + os.path.basename(in_file.name) + concat_str(data.decode('utf-8'))  # just for demonstration
    else:
        message = concat_str(command, params)
    # ---------demo-------------
    send_message(OWN_ADDR, 'S', message)


def command_line():
    while True:
        message = ''
        command = input()
        command_array = command.split()
        if command == '' or valid_command(command_array):  # hibát dob ha nem létező parancsot ad meg a user
            pass
        else:
            make_message(command_array[0], command_array[1:])




def c_incoming(msg):
    print('Incoming message: ' + str(msg, 'utf-8'))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    x = threading.Thread(target=receiver_t)
    x.start()
    command_line()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/


  # elif command_array[0].upper() == valid_commands[0]:  # LGN
        #     print('he')
        #     pass
        #     # TODO
        #
        # elif command_array[0].upper() == valid_commands[1]:  # LGO
        #     pass
        #     # TODO
        #
        # elif command_array[0].upper() == valid_commands[2]:  # MKD
        #     if len(command_array) == 2:  # ha kettő hosszú akkor van benne egy paraméter.
        #         message = concat_str(command_array)
        #         send_message(OWN_ADDR, 'S', message)
        #     else:
        #         print("Error - bad parameter")
        #
        # elif command_array[0].upper() == valid_commands[8]: # UPL
        #     if len(command_array) == 2:  # ha kettő hosszú akkor van benne egy paraméter.
        #         in_file = open(command_array[1], "rb")  # opening for [r]eading as [b]inary
        #         data = in_file.read()
        #         in_file.close()
        #         message = 'upl' + os.path.basename(in_file.name) + concat_str(data.decode('utf-8')) # just for demonstration
        #         send_message(OWN_ADDR, 'S', message)
        #     else:
        #         print("Error - bad parameter")
        #
        # else:
        #     message = concat_str(command_array)
        #     send_message(OWN_ADDR, 'S', message)