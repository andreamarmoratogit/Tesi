import numpy as np;
import socket
import pickle
from time import sleep
import struct
import sys
import time
from sklearn import metrics
from sklearn.cluster import DBSCAN


def receiveData(ipCloud, port,n):
    s = socket.socket()
    s.bind((ipCloud, port))
    s.listen(n)
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
    dataAgg = np.frombuffer(data, dtype=np.float64).reshape(row, -1)

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
        data = np.frombuffer(data, dtype=np.float64).reshape(row, -1)
        print(f"[+] data received from: {addr} with size: {data.shape}")

        dataAgg = np.concatenate((dataAgg, data), axis=0)
        conn.close()
    s.close()
    return dataAgg



print("[+] cloud started")
tStart = time.time()
numDevice = int(sys.argv[1])
eps = int(sys.argv[2])
minPts = int(sys.argv[3])
hostname=socket.gethostname()

ipCloud = socket.gethostbyname(hostname)
print(f"[+] ip = {ipCloud}")
portC = 50000
portE = 50000

print(f"receiveData start:{time.time()-tStart}")
data = receiveData(ipCloud, portC, numDevice)
print(f"receiveData end:{time.time()-tStart}")
x = data[:,:-1]
y = data[:,-1]

print(x[:10])
print(y[:10])
db = DBSCAN(eps=eps, min_samples=minPts).fit(x)
y_sklearn = db.labels_
print("results")
print(y_sklearn[:10])

print(f"Homogeneity: {metrics.homogeneity_score(y, y_sklearn):.3f}")
print(f"Completeness: {metrics.completeness_score(y, y_sklearn):.3f}")
print(f"V-measure: {metrics.v_measure_score(y, y_sklearn):.3f}")
print(f"Adjusted Rand Index: {metrics.adjusted_rand_score(y, y_sklearn):.3f}")
print(f"Adjusted Mutual Information: {metrics.adjusted_mutual_info_score(y, y_sklearn):.3f}")
print(f"Silhouette Coefficient: {metrics.silhouette_score(x, y_sklearn):.3f}")

















