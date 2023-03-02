import socket

SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 4096 # send 4096 bytes each time step

# the ip address or hostname of the server, the receiver
host = "172.17.0.3"
# the port, let's use 5001
port = 5001
# the name of file we want to send, make sure it exists
data = "hello world"
# get the file size
filesize = 15

s = socket.socket()

print(f"[+] Connecting to {host}:{port}")
s.connect((host, port))
print("[+] Connected.")


s.send(f"{data}{SEPARATOR}{filesize}".encode())

s.close()