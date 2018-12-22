import socket
import sys
from functions import *


def main():
    # TODO what if client enters a hostname
    if len(sys.argv) == 5:
        server_addr = sys.argv[1]
        server_port = sys.argv[2]
        function = sys.argv[3]
        srv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        srv_sock.connect((server_addr, int(server_port)))
    else:
        print('Error: Invalid Number of arguments.')
    try:
        status = False
        if function == 'get':
            filepath = sys.argv[4]
            commandline = function + ' ' + filepath
            srv_sock.send(commandline.encode())
            status = file_receive(filepath, srv_sock)
        elif function == 'put':
            filepath = sys.argv[4]
            commandline = function + ' ' + filepath
            srv_sock.send(commandline.encode())
            status = file_sent(filepath, srv_sock)
        elif function == 'list':
            srv_sock.send(b'list')
            data = srv_sock.recv(1024)
            while data != b'':
                print(data.decode())
                data = srv_sock.recv(1024)
            status = True
        else:
            print('Error: Invalid function')
        # logging and reporting
        request = commandline
        request_report(cli_addr, svr_port, request, status)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()
