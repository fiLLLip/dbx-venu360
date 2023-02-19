import socket
import time


def recv_timeout(sock: socket,timeout=1):
    #make socket non blocking
    sock.setblocking(0)
    
    #total data partwise in an array
    total_data=[]
    data=''
    
    #beginning time
    begin=time.time()
    while 1:
        #if you got some data, then break after timeout
        if total_data and time.time()-begin > timeout:
            break
        
        #if you got no data at all, wait a little longer, twice the timeout
        elif time.time()-begin > timeout*2:
            break
        
        #recv something
        try:
            data = str(sock.recv(8192), "utf-8")
            if data:
                total_data.append(data)
                #change the beginning time for measurement
                if "\n" in data:
                    break
                                
                begin = time.time()
            else:
                #sleep for sometime to indicate a gap
                time.sleep(0.1)
        except:
            pass
    
    #join all parts to make final string
    return ''.join(total_data)

def send_and_receive(sock: socket, data = None, timeout=1):
    if data is not None:
        sock.sendall(bytes(data + "\n", "utf-8"))    
        print("Sent: {}".format(data))
    received = recv_timeout(sock, timeout=timeout)
    print("Received: {}".format(received))
    return received

def connect(host, port = 19272, password = 'administrator') -> socket:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    send_and_receive(sock) # Read result from opening connection
    send_and_receive(sock, f'connect administrator "{password}"') # Initiate connection to Venu360 as administrator
    return sock