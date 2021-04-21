import os
import shutil
import threading

from netinterface import network_interface
from common_code import send_message, make_message, net_path  # , receiver_thread

commands = ['LGN', 'LGO', 'MKD', 'RMD', 'RMF', 'GWD', 'CWD', 'LST', 'UPL', 'DNL']

NET_PATH = net_path() #'C:/Users/David/PycharmProjects/client'
OWN_ADDR = 'S'
OWN_DB = OWN_ADDR + '_DB'
CURRENT_FOLDER = 'root'


def receiver_t():
    os.system('python C:/Users/David/PycharmProjects/client/receiver.py --addr ' + OWN_ADDR)


def s_incoming(msg):
    print('Incoming message: ' + msg.decode('utf-8'))
    global CURRENT_FOLDER
    db_dir = NET_PATH + '/' + OWN_DB
    cur_f_dir = NET_PATH + '/' + OWN_DB + '/' + CURRENT_FOLDER
    if not os.path.exists(db_dir):
        os.mkdir(db_dir)
    if not os.path.exists(cur_f_dir):
        os.mkdir(cur_f_dir)
    command = msg[0:3]

    # MKD -  creates a directory in the current folder
    if command == commands[2].lower().encode():
        new_folder_dir = db_dir + '/' + CURRENT_FOLDER + '/' + msg[3:].decode()
        if not os.path.exists(new_folder_dir):
            os.mkdir(new_folder_dir)

    # RMD - removes the directory with all files in it without question
    if command == commands[3].lower().encode():
        rm_folder_dir = db_dir + '/' + CURRENT_FOLDER + '/' + msg[3:].decode()
        if os.path.exists(rm_folder_dir):
            try:
                shutil.rmtree(rm_folder_dir)
            except OSError as e:
                print("Error: %s - %s." % (e.filename, e.strerror))

    # RMF - removes file without question
    if command == commands[4].lower().encode():
        rm_file_dir = db_dir + '/' + CURRENT_FOLDER + '/' + msg[3:].decode()
        if os.path.exists(rm_file_dir):
            os.remove(rm_file_dir)

    # GWD - prints the name of the current folder
    if command == commands[5].lower().encode():
        send_message(OWN_ADDR, 'C', 'Current_folder:_' + CURRENT_FOLDER)

    # CWD - Makes the given folder the current folder, “..” steps back one in the file hierarchy
    if command == commands[6].lower().encode():
        if msg[3:] == b'..':
            string = CURRENT_FOLDER.split('/')
            if len(string) > 1:
                CURRENT_FOLDER = CURRENT_FOLDER[:CURRENT_FOLDER.rfind("/")]
        else:
            folder_dir = db_dir + '/' + CURRENT_FOLDER + '/' + msg[3:].decode()
            if os.path.exists(folder_dir):
                CURRENT_FOLDER += '/' + msg[3:].decode()

        send_message(OWN_ADDR, 'C', 'Current_folder:_' + CURRENT_FOLDER)
        print(CURRENT_FOLDER)

    # LST - list the content of the current folder
    if command == commands[7].lower().encode():
        list_d = '_'.join(map(str, os.listdir(cur_f_dir))) # a listát egy stringé joinolja '_' jelekkel
        if len(os.listdir(cur_f_dir)) == 0:
            list_d = '_'
        send_message(OWN_ADDR, 'C', list_d)

    # UPL - Client-side encryption using AES128-GCM and uploads the file to the current folder
    if command == commands[8].lower().encode():
        f = open(cur_f_dir + '/' + "teszt.txt", "w")
        data = msg[3:].decode('utf-8')
        f.write(data)
        f.close()

    # DNL - downloads the encrypted file to the download folder - decrypts it if key given
    if command == commands[9].lower().encode():
        in_file = open(cur_f_dir + '/' + msg[3:].decode('utf-8'), "rb")  # opening for [r]eading as [b]inary
        data = in_file.read()
        in_file.close()
        send_message(OWN_ADDR, 'C', data.decode('utf-8'))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    x = threading.Thread(target=receiver_t)
    x.start()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/