import numpy as np;
import socket
import pickle
import os.path as osp
from time import sleep
import struct
import sys


def sendToCloud(data,ipCloud, port):
    s = socket.socket()
    print(f"[+] Connecting to {ipCloud}:{port}")
    connected = False
    while not connected:
        try:
            s.connect((ipCloud, port))
            connected = True
        except socket.error:
            sleep(2)
    print("[+] Connected.")
    length = struct.pack('>Q',data.nbytes)
    nrow = struct.pack('>Q',len(data))
    s.sendall(length)
    s.sendall(nrow)
    s.sendall(data.tobytes())
    s.close()
    


print("edge started")
ipCloud = "172.21.0.2"
datasetName = sys.argv[1]
portE = 50000
portC = 50000

path = osp.dirname(osp.realpath("__file__"))
data = np.loadtxt(path+"/"+datasetName,delimiter=",", dtype=float)
print(data[:19])
print(data.shape)
print(data.dtype)
#x = data[:,:-1]
#y = data[:,-1]

sendToCloud(data,ipCloud, portC)
print("[+] sended")
