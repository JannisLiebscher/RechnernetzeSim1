import socket
import struct
import threading
import codecs


global Clients
Clients = []


def updateAllClients():
    global Clients
    for c in Client_Sockets:
        responce = getString()
        r = str.encode(responce)
        # Sende das Ergebnis an den Client
        c.send(r)


def getString():
    global Clients
    ClientString = []
    for s in Clients:
        for item in s:
            ClientString.append(item)
            ClientString.append('|')
    responce = " ".join(str(x) for x in ClientString)
    return responce

def handle_client(clinent_socket):
    run = True
    while run:
        # Empfange die Anfrage
        responce = clinent_socket.recv(1024)
        # Anfrage Dekodieren
        operation = responce.decode('utf-8')
        print("der Server hat eine Nachricht erhalten: " + str(operation))
        information  = str(operation).split('|')

        operation = information[0]
        Nickname = information[1]
        IPAdress = information[2]
        UDPPort = information[3]

        if(operation == "Login"):
            global Clients
            Clients.append((Nickname,IPAdress,UDPPort))
            ans = "Success".encode('utf-8')
            clinent_socket.send(ans)
            updateAllClients()

        run = False

Client_Sockets = []

IP_Server = 'localhost'
Port_Server = 10000

# Erstelle einen TCP/IP-Socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Binde den Socket an eine Adresse und einen Port
server_address = (IP_Server, Port_Server)
sock.bind(server_address)

# Lausche auf eingehende Verbindungen (maximal 1)
print("Horche auf Verbindung")
sock.listen(5)

while True:
    # Akzeptiere eine eingehende Verbindung
    print("Akzeptiere Verbindung")
    client_socket, client_address = sock.accept()
    Client_Sockets.append(client_socket)
    client_thread = threading.Thread(target=handle_client, args=(client_socket,))
    client_thread.start()