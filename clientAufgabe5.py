import socket
import struct
import threading
import time

echo = True
ip = '141.37.168.26'
protocol = 'UDP'

# Verbinde den Socket mit dem Server
def connect(port):
    try:
        if protocol == 'TCP':
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_address = (ip, port)
        sock.connect(server_address)
        print("Verbindung erfolgreich für Port " + str(port))
        if echo:
            sock.send("test")
            re = sock.recv(1024)
            print("return value = "+ str(re))
        sock.close()
    except Exception as e:
            print(str(e) + " " +str(port)+ "\n")

print("Verbinde den Socket mit dem Server")
if not echo:
    for i in range(1,51):
        thread = threading.Thread(target=connect, args=(i,))
        thread.start()
else:
    thread = threading.Thread(target=connect, args=(7,))
    thread.start()


# keine Rückmeldung für TCP ports keine
# UDP alle Verbindungen erfolgreich
# Aufgabe 5 noch machen
# Wireshark aufzeichnen(5.21)
