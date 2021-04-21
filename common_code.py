import os


def net_path():
    return os.getcwd() #'C:/Users/David/PycharmProjects/client'


def send_message(addr, dst, msg):
    os.system('python C:/Users/David/PycharmProjects/client/sender.py --addr ' + addr + ' --dst ' + dst
              + ' --msg ' + msg)


# def receiver_thread(addr):
# os.system('python C:/Users/David/PycharmProjects/client/receiver.py --addr ' + addr)

def concat_str(command, params):
    # temporary
    str = command
    for x in params:
        str += x
        # print(str)
    return str
