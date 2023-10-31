import socket
import time
import json
import struct

# Create a TCP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# IP and port to listen on
server_address = ('localhost', 12345)
sock.bind(server_address)
sock.listen(1)

print("Waiting for a connection...")
connection, client_address = sock.accept()
print("Connected to:", client_address)

f=True
d=json.loads(connection.recv(8192).decode())
p=struct.unpack('!i', connection.recv(4))[0]
print(d)
time.sleep(1)
b=-1
while True:
    a=struct.unpack('!i', connection.recv(4))[0]
    x=str(a)
    if a==-2:
        break
    if x in d.keys() and d[x]:
        d[x]=False
    else:
        print("Packet ",a," received")
        time.sleep(1)
        if a-1==b:
            b=a
            connection.send(struct.pack("!i",a))
            print("Acknowledgement ",a," sent")
        else:
            connection.send(struct.pack("!i",b))
            print("Acknowledgement ",b," sent")

    time.sleep(1)
    
print("Connection Ended")
# Close the connection and socket
connection.close()
sock.close()
