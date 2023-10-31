import socket
import time

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
p=connection.recv(1024).decode()
d={"2":True,"5":True,"7":True}
time.sleep(1)
b=-1
while True:
    a=connection.recv(1).decode()
    if a=="$":
        break
    if a in d.keys() and d[a]:
        d[a]=False
    else:
        print("Packet "+a+" received")
        time.sleep(1)
        if int(a)-1==b:
            b=int(a)
            connection.send(str.encode(a))
            print("Acknowledgement "+a+" sent")
        else:
            connection.send(str.encode(str(b)))
            print("Acknowledgement ",b," sent")

    time.sleep(1)
    
print("Connection Ended")
# Close the connection and socket
connection.close()
sock.close()
