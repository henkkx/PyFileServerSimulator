import socket
import sys
from functions import *


def main():
    # ip, port and directory details
    svr_addr = socket.gethostbyname(socket.gethostname())
    svr_port = sys.argv[1]
    svr_path = os.path.dirname(os.path.abspath(__file__))

    print('IPv4 Address {}'.format(svr_addr))
    print('port number: {}'.format(svr_port))
    print('server path: {}'.format(svr_path))

    try:
        # sys.argv[1] is the port number
        # server will listen for connections on input port
        srv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        srv_sock.bind(('0.0.0.0', int(svr_port)))
        srv_sock.listen(5)
    except Exception as e:
        print(e)
        exit(1)

    while True:
        try:
            print("Waiting for client... ")
            cli_sock, cli_addr = srv_sock.accept()
            # Translate the client address to a string (to be used shortly)
            cli_addr_str = str(cli_addr)
            print("Client " + cli_addr_str + " connected.")

            while True:
                status = False
                commandline = cli_sock.recv(1024).decode()
                if len(commandline) != 0:
                    command = commandline[:4].strip().lower()
                    filepath = commandline[4:].strip()
                    if command == 'get':
                        status = file_sent(filepath, cli_sock)
                    elif command == 'put':
                        status = file_receive(filepath, cli_sock)
                    elif command == 'list':
                        status = listdirectory(cli_sock)
                    else:
                        cli_sock.send(b'Error: Invalid command')
                        status = False
                    # logging and reporting.
                    request = commandline
                    request_report(cli_addr, svr_port, request, status)
                print('Client ' + cli_addr_str + ' disconnected.')
                cli_sock.close()
                break
        except Exception as e:
            """
             If an error occurs or the client closes the connection,
             call close() on the connected socket
             to release the resources allocated to it by the OS.
            """
            print(e)
    # Close the server socket as well to release its resources back to the OS
    srv_sock.close()
    # Exit with a zero value, to indicate success
    exit(0)


if __name__ == '__main__':
    main()
