import socket
import struct
import time
import codecs

def splitString(result):
    ClientStrings = result.split('|')

    Clients = []

    counter = 0
    newList = []
    for string in ClientStrings:
        if counter == 2:
            Clients.append((newList[0], newList[1], string))
            counter = 0
            newList = []
        else:
            newList.append(string)
            counter = counter + 1
    return Clients



# Erstelle einen TCP/IP-Socket
sock= socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_address = ('localhost', 1300)
sock.bind(client_address)

# Verbinde den Socket mit dem Server
print("Verbinde den Socket mit dem Server")
server_address = ('localhost', 10000)
sock.connect(server_address)

# Erstelle die Anfrage-Nachricht
id = 1
operation = "Login|Client1|localhost|1300" # Nickname, IP Adresse und UDP Port


# Packe die Anfrage-Nachricht als Bytes-Objekt
#request = struct.pack("!I8sB",operation)
request = str.encode(operation)
#Anmelden beim Server
sock.sendall(request)

#Warte auf die Bestätigung
response = sock.recv(1024)
print("client wurde beim Server angemeldet ")

result = response.decode('utf-8')
print("Result:", result)
Clients = splitString(result)


run = True
while run==True:
    sock.accept()
    response = sock.recv(1024)
    result = response.decode('utf-8')
    Clients = splitString(result)

sock.close