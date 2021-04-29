import os
import shutil
import threading

from Crypto.Util.Padding import unpad

from netinterface import network_interface
from common_code import send_message, concat_str, net_path  # , receiver_thread
from sender import send_message
import commands
from Crypto.Random import get_random_bytes
import ownRSA
from Crypto.Cipher import AES


class Server:

    OWN_ADDR = 'S'
    cert_path = "keys\server_cert.crt"
    key_path = "keys\server_key.pem"
    passphrase = 'lofasz'
    SQN = 1
    session_token = b''
    session_key = b''
    # f.NET_PATH = net_path() #'C:/Users/David/PycharmProjects/client'
    # f.OWN_ADDR = 'S'
    OWN_DB = OWN_ADDR + '_DB'
    CURRENT_FOLDER = 'root'
    cert = b''
    cert = b''
    rnd = b''
    initialized = False
        

        
    # commands = ['LGN', 'LGO', 'MKD', 'RMD', 'RMF', 'GWD', 'CWD', 'LST', 'UPL', 'DNL']

def get_cert_and_rnd():
    try:
        with open(Server.cert_path, "rb") as server_cert_file:
            Server.cert = server_cert_file.read()

            Server.rnd = get_random_bytes(16) # random generation
            return Server.cert + Server.rnd

    except (FileNotFoundError) as e:
        print('ERROR:' + e)
        return False


def receiver_t():
        os.system('python ' + net_path() + '\\receiver.py --addr ' + Server.OWN_ADDR)

def priv_key_check(ciphertext):
     # if ha elbaszna
    plaintext = ownRSA.priv_decrypt(ciphertext, Server.key_path, Server.passphrase)
    Server.session_token = plaintext[:16]
    Server.session_key = plaintext[16:32]
    rand = plaintext[32:]
    print(plaintext)
    if rand != Server.rnd:
        print('Not the same random')
        return False
    return True 

def key_exchange_init(msg):
    print(msg)
    if msg[:3].upper().decode() == commands.BGN:
        make_message('', '', get_cert_and_rnd(), '')
    elif msg[:3].upper().decode() == 'PUB':
        if priv_key_check(msg[3:]):
            send_GCM_session_token()
            # make_message(type, err, res, file)


def s_incoming(msg):
    # ---------demo-------------
    if Server.initialized:
        process(msg[:3], msg[3:])
    else:
        key_exchange_init(msg)
    # ---------demo-------------

def send_GCM_session_token():

    SQN_b = Server.SQN.to_bytes(4, byteorder = 'big')
    RND = get_random_bytes(8)
    nonce = SQN_b + RND
    cipher = AES.new(Server.session_key, AES.MODE_GCM, nonce=nonce)
    ciphertext, tag = cipher.encrypt_and_digest(Server.session_token)
    msg_len = (len(SQN_b + RND + ciphertext + tag) + 2).to_bytes(2, byteorder = 'big')
    msg =  msg_len + SQN_b + RND + ciphertext + tag
    send_message(msg, Server.OWN_ADDR, 'C')


def make_message(type, err, res, file):
    # IDE JÖN A TITKOSÍTÁS
    send_message(res, Server.OWN_ADDR, 'C')
    #send_message(OWN_ADDR, 'C', res)


def process(cmd, param):
    Server.SQN = Server.SQN+1
    print(Server.SQN)
    print('Incoming message: ' + cmd.decode('utf-8'))
    db_dir = net_path() + '/' + Server.OWN_DB
    cur_f_dir = net_path() + '/' + Server.OWN_DB + '/' + Server.CURRENT_FOLDER
    if not os.path.exists(db_dir):
        os.mkdir(db_dir)
    if not os.path.exists(cur_f_dir):
        os.mkdir(cur_f_dir)
    command = cmd.upper().decode()
    # MKD -  creates a directory in the current folder
    if command == commands.MKD:
        new_folder_dir = db_dir + '/' + Server.CURRENT_FOLDER + '/' + param.decode()
        if not os.path.exists(new_folder_dir):
            os.mkdir(new_folder_dir)

    # RMD - removes the directory with all files in it without question
    elif command == commands.RMD:
        rm_folder_dir = db_dir + '/' + Server.CURRENT_FOLDER + '/' + param.decode()
        if os.path.exists(rm_folder_dir):
            try:
                shutil.rmtree(rm_folder_dir)
            except OSError as e:
                print("Error: %s - %s." % (e.filename, e.strerror))

    # RMF - removes file without question
    elif command == commands.RMF:
        rm_file_dir = db_dir + '/' + Server.CURRENT_FOLDER + '/' + param.decode()
        if os.path.exists(rm_file_dir):
            os.remove(rm_file_dir)

    # GWD - prints the name of the current folder
    elif command == commands.GWD:
        make_message('', '', b'Current_folder:_' + Server.CURRENT_FOLDER.encode(), '')

    # CWD - Makes the given folder the current folder, “..” steps back one in the file hierarchy
    elif command == commands.CWD:
        if param == b'..':
            string = Server.CURRENT_FOLDER.split('/')
            if len(string) > 1:
                Server.CURRENT_FOLDER = Server.CURRENT_FOLDER[:Server.CURRENT_FOLDER.rfind("/")]
        else:
            folder_dir = db_dir + '/' + Server.CURRENT_FOLDER + '/' + param.decode()
            if os.path.exists(folder_dir):
                Server.CURRENT_FOLDER += '/' + param.decode()

        make_message('', '', b'Current_folder:_' + Server.CURRENT_FOLDER.encode(), '')
        print(Server.CURRENT_FOLDER)

    # LST - list the content of the current folder
    elif command == commands.LST:
        list_d = '_'.join(map(str, os.listdir(cur_f_dir))) # a listát egy stringé joinolja '_' jelekkel
        if len(os.listdir(cur_f_dir)) == 0:
            list_d = '_'
        make_message('', '', list_d.encode(), '')

    # UPL - Client-side encryption using AES128-GCM and uploads the file to the current folder
    elif command == commands.UPL:
        if len(param) >= 44:
            enc_message = param
            print(enc_message)
            if enc_message[15] == 128 or enc_message[15] == 0:
                file_name = unpad(enc_message[:16], 16, 'iso7816').decode('ascii')
            else:
                file_name = enc_message[:16].decode('ascii')
            nonce = enc_message[16:28]
            ciphertext = enc_message[28:-16]
            tag = enc_message[-16:]
            data = nonce + ciphertext + tag
            # end_of_data = len(param)-16
            # file_name = param[:16].decode('utf-8')
            # nonce = param[16:28]
            # data = param[28:end_of_data].decode('utf-8')
            # tag = param[end_of_data:]
            f = open(cur_f_dir + '/' + file_name, "wb")
            f.write(data)
            f.close()
        else:
            print('Error - To short file...')

    # DNL - downloads the encrypted file to the download folder - decrypts it if key given TODO: megvan ez?
    elif command == commands.DNL :
        in_file = open(cur_f_dir + '/' + param.decode('utf-8'), "rb")  # opening for [r]eading as [b]inary
        data = in_file.read()
        in_file.close()
        make_message('', '', data.decode('utf-8'), '')
    


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # s = Server(passphrase='lofasz')
    x = threading.Thread(target=receiver_t)
    x.start()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/