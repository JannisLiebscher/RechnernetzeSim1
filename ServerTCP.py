import socket
import time
import struct
import numpy

My_IP = '127.0.0.1'
My_PORT = 50000
server_activity_period=30

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((My_IP, My_PORT))
print('Listening on Port ',My_PORT, ' for incoming TCP connections');

t_end=time.time()+server_activity_period

sock.listen(1)
print('Listening ...')

while time.time()<t_end:
    try:
        conn, addr = sock.accept()
        print('Incoming connection accepted: ', addr)
        break
    except socket.timeout:
        print('Socket timed out listening',time.asctime())

while time.time()<t_end:
    try:
        data = conn.recv(1024)
        if not data:
            print('Connection closed from other side');
            print('Closing ...');
            conn.close()
            break
        print('received message: ', data.decode('utf-8'), 'from ', addr)
        response = str(data).split()
        newList = []
        for i in range(int(response[2])):
            newList.append(int(response[i + 3]))

        if response[1] == "Summe":
            conn.send(response[0])
            int2 = " " + str(sum(newList))
            conn.send(int2)
        if response[1] == "Produkt":
            conn.send(response[0])
            int2 = " " + str(numpy.prod(newList))
            conn.send(int2)
        if response[1] == "Maximum":
            conn.send(response[0])
            conn.send(" " + str(max(newList)))
        if response[1] == "Minimum":
            conn.send(response[0])
            conn.send(" " + str(max(newList)))
    except socket.timeout:
        print('Socket timed out at',time.asctime())

sock.close()
if conn:
    conn.close()
