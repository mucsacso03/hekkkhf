import os
import shutil
import threading

from netinterface import network_interface
from common_code import send_message, concat_str, net_path  # , receiver_thread
from sender import send_message

commands = ['LGN', 'LGO', 'MKD', 'RMD', 'RMF', 'GWD', 'CWD', 'LST', 'UPL', 'DNL']

NET_PATH = net_path() #'C:/Users/David/PycharmProjects/client'
OWN_ADDR = 'S'
OWN_DB = OWN_ADDR + '_DB'
CURRENT_FOLDER = 'root'


def receiver_t():
    os.system('python ' + net_path() + '\\receiver.py --addr ' + OWN_ADDR)


def s_incoming(msg):
    # ---------demo-------------
    process(msg[:3], msg[3:])
    # ---------demo-------------


def make_message(type, err, res, file):
    send_message(res.encode(), OWN_ADDR, 'C')
    #send_message(OWN_ADDR, 'C', res)


def process(cmd, param):
    print('Incoming message: ' + cmd.decode('utf-8'))
    global CURRENT_FOLDER
    db_dir = NET_PATH + '/' + OWN_DB
    cur_f_dir = NET_PATH + '/' + OWN_DB + '/' + CURRENT_FOLDER
    if not os.path.exists(db_dir):
        os.mkdir(db_dir)
    if not os.path.exists(cur_f_dir):
        os.mkdir(cur_f_dir)
    command = cmd

    # MKD -  creates a directory in the current folder
    if command == commands[2].lower().encode():
        new_folder_dir = db_dir + '/' + CURRENT_FOLDER + '/' + param.decode()
        if not os.path.exists(new_folder_dir):
            os.mkdir(new_folder_dir)

    # RMD - removes the directory with all files in it without question
    elif command == commands[3].lower().encode():
        rm_folder_dir = db_dir + '/' + CURRENT_FOLDER + '/' + param.decode()
        if os.path.exists(rm_folder_dir):
            try:
                shutil.rmtree(rm_folder_dir)
            except OSError as e:
                print("Error: %s - %s." % (e.filename, e.strerror))

    # RMF - removes file without question
    elif command == commands[4].lower().encode():
        rm_file_dir = db_dir + '/' + CURRENT_FOLDER + '/' + param.decode()
        if os.path.exists(rm_file_dir):
            os.remove(rm_file_dir)

    # GWD - prints the name of the current folder
    elif command == commands[5].lower().encode():
        make_message('', '', 'Current_folder:_' + CURRENT_FOLDER, '')

    # CWD - Makes the given folder the current folder, “..” steps back one in the file hierarchy
    elif command == commands[6].lower().encode():
        if param == b'..':
            string = CURRENT_FOLDER.split('/')
            if len(string) > 1:
                CURRENT_FOLDER = CURRENT_FOLDER[:CURRENT_FOLDER.rfind("/")]
        else:
            folder_dir = db_dir + '/' + CURRENT_FOLDER + '/' + param.decode()
            if os.path.exists(folder_dir):
                CURRENT_FOLDER += '/' + param.decode()

        make_message('', '', 'Current_folder:_' + CURRENT_FOLDER, '')
        print(CURRENT_FOLDER)

    # LST - list the content of the current folder
    elif command == commands[7].lower().encode():
        list_d = '_'.join(map(str, os.listdir(cur_f_dir))) # a listát egy stringé joinolja '_' jelekkel
        if len(os.listdir(cur_f_dir)) == 0:
            list_d = '_'
        make_message('', '', list_d, '')

    # UPL - Client-side encryption using AES128-GCM and uploads the file to the current folder
    elif command == commands[8].lower().encode():
        if len(param) >= 44:
            end_of_data = len(param)-16
            file_name = param[:16].decode('utf-8')
            nonce = param[16:28]
            data = param[28:end_of_data].decode('utf-8')
            tag = param[end_of_data:]
            f = open(cur_f_dir + '/' + file_name, "w")
            f.write(data)
            f.close()
        else:
            print('Error - To short file...')

    # DNL - downloads the encrypted file to the download folder - decrypts it if key given
    elif command == commands[9].lower().encode():
        in_file = open(cur_f_dir + '/' + param.decode('utf-8'), "rb")  # opening for [r]eading as [b]inary
        data = in_file.read()
        in_file.close()
        make_message('', '', data.decode('utf-8'), '')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    x = threading.Thread(target=receiver_t)
    x.start()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
