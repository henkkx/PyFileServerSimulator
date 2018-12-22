import os


def file_sent(filename, sock):
    '''
    Sents a file as a stream of bytes to a socket
    '''
    # status variable is set to true once file sending is completed correctly
    # to be used later for reporting
    status = False
    try:
        if os.path.isfile(filename):
            if len(filename) > 50:
                print('Error: File name is too long.')
            else:
                # cannot transfer executable files for security reasons
                if filename.endswith('.exe'):
                    print('Error: Cannot send executable file')
                else:
                    filesize = os.path.getsize(filename)
                    # cannot sent empty or too large files
                    if filesize == 0:
                        print('Error: cannot sent empty file.')
                    else:
                        if filesize > 300000000:
                            print('Error: File is too large.')
                        else:
                            sock.send(str(filesize).encode())
                            with open(filename, 'rb') as f:
                                bytes_to_send = f.read(1024)
                                while len(bytes_to_send) != 0:
                                    sock.send(bytes_to_send)
                                    bytes_to_send = f.read(1024)
                            print('File {}, size: {} sent'.format(filename, filesize))
                            status = True
        else:
            print('Error: could not find file.')

    except Exception as e:
        print(e)
    return status


def file_receive(filename, sock):
    '''
    Receives a file as a stream of bytes from a socket
    '''

    # status variable is set to true once file receiving is completed correctly
    # to be used later for reporting
    status = False
    try:
        # cannot allow overwriting files.
        if os.path.exists(filename):
            print('Error: cannot overwrite file.')
        else:
            if len(filename) > 50:
                print('Error: File name is too long.')
            else:
                # cannot receive executable file for security reasons.
                if filename.endswith('.exe'):
                    print('Error: Cannot receive executable file.')
                else:
                    filesize = sock.recv(1024)
                    filesize = int(filesize.decode())
                    # zero-sized files cannot be transferred.
                    if filesize == 0:
                        print('Error: File cannot have size 0')
                    else:
                        # too large files e.g 300 MB cannot be transferred.
                        if filesize > 300000000:
                            print('Error: File is too large.')
                        else:
                            file_length = 0
                            # creates a new binary file and write
                            # received bytes into it until the
                            # file length of the file been written is the same
                            # with the bytes sent.
                            with open(filename, 'wb') as f:
                                while file_length < filesize:
                                    bytes_to_recv = sock.recv(1024)
                                    f.write(bytes_to_recv)
                                    file_length += len(bytes_to_recv)
                            print('file {} received, size: {}'.format(filename, filesize))
                            status = True
    except Exception as e:
        print(e)
    return status


def listdirectory(sock):
    #  sends current directory contents
    for stuff in os.listdir():
        print(stuff)
        sock.send(stuff.encode())
    return True


def request_report(cli_addr, cli_port, request, status):
    '''
    print a report of a client request to server terminal
    '''
    if status:
        print('Report: {} {}, Success'.format(cli_addr, request))
    else:
        print('Report: {} {}, Failure'.format(cli_addr, request))
