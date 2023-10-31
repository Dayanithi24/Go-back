import socket
import time
import select
import struct
import json

# Create a TCP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# IP and port of the receiver (server)
server_address = ('localhost', 12345)

# Connect to the server
sock.connect(server_address)

buffer_size=8192

p=int(input("Enter the total number of packets: "))
ws=int(input("Enter the Window Size: "))
arr=list(map(int,input("Enter the packets to be dropped : ").split()))
print(arr)
d={}
for k in arr:
    d[k]=True
print(d)
sock.sendall(json.dumps(d).encode())
i=0
a=[[j,True] for j in range(ws)]
c=0

sock.send(struct.pack("!i",p-1))
sock.setblocking(0)

while i<p:
    try:
        k, _, _ = select.select([sock], [], [], 2)
        for j in range(len(a)):
            if a[j][1]:
                sock.send(struct.pack("!i",a[j][0]))
                a[j][1]=False
                print("Packet %d sent.."%a[j][0])
                c+=1
            time.sleep(1)
        print(a)
        b=struct.unpack('!i', sock.recv(4))[0]
        if b==a[0][0]:
            print("Acknowlwdgement ",b," received..")
            if(i<p-ws):
                a=a[1:]+[[i+ws,True]]
            else:
                a=a[1:]
            i+=1
        else:
            print("Acknowlwdgement ",b," received..")
    except:
        print("************* Session Timed Out *************")
        for j in range(len(a)):
           a[j][1]=True
        time.sleep(2)

sock.send(struct.pack("!i",-2))
print("Total no.of transmissions = %d"%c)
# Close the socket
sock.close()
