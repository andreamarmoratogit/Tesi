"""EDGE DEVICE"""
import numpy as np;
import matplotlib.pyplot as plt
import os.path as osp
from sklearn.model_selection import train_test_split
import socket
import pickle
import struct
from time import sleep
from sklearn import metrics




def width(X):
    min = X.min(axis = 0)
    max = X.max(axis = 0)
    return np.stack((min,max))

#discretizzazione dei valori rispetto al numero di bin prefissato
def minMaxBinner(X,min,max,numBin):
    n = X.shape[0]
    width=np.abs(max-min)/numBin
    res = (X - min) / width
    res = np.c_[res,np.ones(n,int)].astype(int)
    return res

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
    
def receiveClusterDict(port):
    s = socket.socket()
    hostname=socket.gethostname()
    localIp=socket.gethostbyname(hostname)
    s.bind((localIp,port))
    s.listen()
    conn,addr = s.accept()
    data = b''
    while True:
        chunk = conn.recv(4096)
        if not chunk:
            break
        data += chunk
    deserDict = pickle.loads(data)
    conn.close()
    s.close()  
    return deserDict



print("edge started")
numBin = 23
minPts = 10
ipCloud = "172.20.0.2"
port = 50000

path = osp.dirname(osp.realpath("__file__"))
#caricamento dati di test
data = np.loadtxt(path+'/data3.csv',delimiter=",", dtype=float)

x1,x2,y1,y2 = train_test_split(data[:,:-1],data[:,-1], test_size=0.5, random_state=42)

#calcolo valori di massimi e minimi locali
w1 = width(x1)
w2 = width(x2)

#plot dei dati
#plt.scatter(x1[:,0], x1[:,1], s=3)
#plt.scatter(x2[:,0], x2[:,1], s=3)
#plt.show()


sendToCloud(w2,ipCloud, port)
print("[+] sended")


#receive response
s = socket.socket()
hostname=socket.gethostname()
localIp=socket.gethostbyname(hostname)
print(f"[+] listening at: {localIp}")
s.bind((localIp,port))
s.listen()
conn,addr = s.accept()
resp = conn.recv(4096)
mTot = pickle.loads(resp)
conn.close()
s.close()
print(f"[+] data received: {mTot}")

#aggregation
disc = minMaxBinner(x1, mTot[0], mTot[1], numBin)
discAgg = aggregation(disc,numBin)    
sendToCloud(discAgg,ipCloud, port)
print(f"[+] aggregated data sended: {discAgg.shape}")

clusterDict = receiveClusterDict(port)

y1_pred = [ clusterDict.get(tuple(i[:-1]),-1) for i in disc ]

#scatter = plt.scatter(x1[:,0], x1[:,1], c = y1_pred, s=3)

print("\nRESULTS:")
print(f"Homogeneity: {metrics.homogeneity_score(y1, y1_pred):.3f}")
print(f"Completeness: {metrics.completeness_score(y1, y1_pred):.3f}")
print(f"V-measure: {metrics.v_measure_score(y1, y1_pred):.3f}")
print(f"Adjusted Rand Index: {metrics.adjusted_rand_score(y1, y1_pred):.3f}")
print(f"Adjusted Mutual Information: {metrics.adjusted_mutual_info_score(y1, y1_pred):.3f}")
print(f"Silhouette Coefficient: {metrics.silhouette_score(x1, y1_pred):.3f}")