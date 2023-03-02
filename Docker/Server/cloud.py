import numpy as np;
#import matplotlib.pyplot as plt
#import os.path as osp
#from sklearn.model_selection import train_test_split
import socket
import pickle
from time import sleep
import struct
import sys

def sendMinMaxToEdge(addrs,mTot,port):
    for addr in addrs:
        s = socket.socket()
        sended = False
        while not sended:
            try:
                print(f"[+] try to connect to {addr}")
                s.connect((addr[0],port))
                sended = True
            except socket.error:
                sleep(2)
                
        print("[+] Connected.")
        s.sendall(pickle.dumps(mTot))
        s.close()
    
def receiveMinMax(ipCloud, port,n):
    
    addrs = []
    minTot = np.empty((0,2),float)
    maxTot = np.empty((0,2),float)
    for i in range(n):
        s = socket.socket()
        s.bind((ipCloud, port))
        s.listen(1)
        conn, addr = s.accept()
        addrs.append(addr)
        length  = conn.recv(8)
        length = struct.unpack('>Q', length)[0]
        row = conn.recv(8)
        row = struct.unpack('>Q', row)[0]
        print(f"length data: {length}")
        data = b''
        while len(data) < length:
            packet = conn.recv(length - len(data))
            if not packet:
                print("ERRORE")
                continue
            data += packet
        data = np.frombuffer(data, dtype=np.float64).reshape(row, -1)
        print(f"[+] data received from {addr} =  {data}")
        minTot = np.vstack([minTot, data[0]])
        maxTot = np.vstack([maxTot, data[1]])
        conn.close()
        s.close()
    minTot = minTot.min(axis = 0) - 0.01
    maxTot = maxTot.max(axis = 0) + 0.01
    mTot = [minTot,maxTot]
    return addrs,mTot


def receiveDataAgg(ipCloud, port,n):
    s = socket.socket()
    s.bind((ipCloud, port))
    s.listen(1)
    conn, addr = s.accept()
    length  = conn.recv(8)
    length = struct.unpack('>Q', length)[0]
    row = conn.recv(8)
    row = struct.unpack('>Q', row)[0]
    data = b''
    while len(data) < length:
        packet = conn.recv(length - len(data))
        if not packet:
            break
        data += packet

    # Converte i dati ricevuti in un numpy array
    dataAgg = np.frombuffer(data, dtype=np.int64).reshape(row, -1)

    conn.close()
    #s.close()
    print(f"[+] data received from: {addr} with size: {dataAgg.shape}")

    for i in range(n-1):
        #s = socket.socket()
        #s.bind((ipCloud, port))
        #s.listen(1)
        conn, addr = s.accept()
        length  = conn.recv(8)
        length = struct.unpack('>Q', length)[0]
        row = conn.recv(8)
        row = struct.unpack('>Q', row)[0]
        data = b''
        while len(data) < length:
            packet = conn.recv(length - len(data))
            if not packet:
                break
            data += packet

        # Converte i dati ricevuti in un numpy array
        data = np.frombuffer(data, dtype=np.int64).reshape(row, -1)
        print(f"[+] data received from: {addr} with size: {data.shape}")

        dataAgg = np.concatenate((dataAgg, data), axis=0)
        conn.close()
    s.close()
    return dataAgg



#Calcolo degli indici delle celle vicine
def neighborhood(X,el):
    index = np.array([],int)
    for i,n in enumerate(X):
        diff = el[:-2]-n[:-2]
        ok = True
        for j in np.abs(diff):
            if j>1:
                ok = False
        if ok:
            index = np.append(index,i)
    return index

#aggregazione dei dati corrispondenti alla stessa cella
def aggregation(X,numBin):    
    for i in range(numBin**X.shape[1]):
        index = np.array([],int)
        for j in range(i+1,X.shape[0]):
            if(np.array_equal(X[i][:-1],X[j][:-1])):
                X[i][-1]+=X[j][-1]
                index = np.append(index, j)
        X = np.delete(X,index,axis = 0)
    return X

#aloritmo realizzato prendendo spunto dal DBSCAN originale
def DBSCAN(X,numBin,minPts):
    X = aggregation(X, numBin)
    X = np.c_[X,np.zeros(X.shape[0],int)].astype(int)
    c = 0
    for el in X:
        if el[-1]!=0: continue
        if el[-2]<minPts:
            el[-1] = -1
            continue
        c+=1
        el[-1] = c
        n = neighborhood(X,el)  
        k=-1
        while True:
            k+=1
            if k>=n.size: break
            if X[n[k]][-1]==-1: X[n[k]][-1] = c
            if X[n[k]][-1]!=0: continue
            X[n[k]][-1] = c
            if X[n[k]][-2]<minPts:continue
            n2 = neighborhood(X,X[n[k]])
            #n = np.concatenate((n,n2))
            for neighbor in n2:
                if neighbor not in n:
                    n = np.append(n, neighbor)
        
    #rimozione delle celle associate ad anomalie
    index = np.array([],int)
    for i,el in enumerate(X):
        if el[-1]==-1:
            index = np.append(index,i)
    X = np.delete(X,index,axis = 0)
    #costruzione di un dizionario key:value dove la chiave è data dalla cella e il valore è dato dal numero di cluster
    x_tuple=list(map(tuple,X[:,:-2]))
    x_dict=dict(zip(x_tuple,X[:,-1]))
    return x_dict

def sendClusterDict(clusterDict, addrs, port):
    serDict = pickle.dumps(clusterDict)
    for addr in addrs:
        s = socket.socket()
        print(f"[+] Connecting to {addr}")
        connected = False
        while not connected:
            try:
                s.connect((addr[0],port))
                connected = True
            except socket.error:
                sleep(2)
        print("[+] Connected.")
        s.sendall(serDict)
        s.close()
   
"""parameter:
    1 = numDevice 
    2 = numBin (23)
    3 = minPts (10)

"""    

print("[+] cloud started")

numDevice = int(sys.argv[1])
numBin = int(sys.argv[2])
minPts = int(sys.argv[3])
hostname=socket.gethostname()

ipCloud = socket.gethostbyname(hostname)
print(f"[+] ip = {ipCloud}")
port = 50000




addrs,mTot= receiveMinMax(ipCloud, port,numDevice)
print(mTot)

#send to edge
sendMinMaxToEdge( addrs, mTot, port)

print("[+] response sended")

#unione dei dati aggregati forniti dai dispositivi edge
dataAgg = receiveDataAgg(ipCloud, port, numDevice)

print(f"[+] data agg received: {dataAgg}")

#calcolo dei cluster
clusterDict = DBSCAN(dataAgg,numBin,minPts)

sendClusterDict(clusterDict, addrs, port)