import socket
import struct
import threading
import time
import codecs

global Clients
Clients = []

IP_Server = 'localhost'
POTR_Server = 10000

Client_Port_UDP = 1200

CHAT_IP = 'localhost'
CHAT_Port = 1220

myNickname = "client1"

global goOn
goOn = True


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
def update():
    global goOn
    while goOn:
        rec = server.recv(1024)
        ans = rec.decode('utf-8')
        print(ans)
        global Clients
        Clients = splitString(ans)
def chatWithUser(chat):#chatf
    chat.send(b'Hi')
    ans = chat.recv(1024)
    print(ans)

def listenchat(): #listenUDP
    global goOn
    while goOn:
        ans = clientudp.recv(1024)
        rec = ans.decode('utf-8') # Nickname|ip|Port
        con = rec.split('|')
        chat_UDP.connect((con[1],int(con[2])))
        print("connected to User: " + str(con[0]))
        threading.Thread(target=chatWithUser,args=(chat_UDP,)).start()

def tryConnectWithUser(): #send connect with user
    nickname = input('enter Nickname')
    found = False
    for c in Clients:
        if(c[0] == nickname):
            user = c
            found = True
    if found == False:
        print("Nickname nicht gefunden")
        tryConnectWithUser()
    else:
        msg = myNickname + '|' + CHAT_IP + '|' + CHAT_Port
        msg = msg.encode('utf-8')
        clientudp.sendto(msg,(user[1],user[2]))
        chat_UDP.listen(5)
        conn, addr = chat_UDP.accept()
        threading.Thread(target=chatWithUser,args=(conn,)).start()


# Verbindung zum Server
server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.connect((IP_Server,POTR_Server))

# Udp port Bind
clientudp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
clientudp.bind(('',Client_Port_UDP))

chat_UDP = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
chat_UDP.bind((CHAT_IP,CHAT_Port))


# Erstelle die Anfrage-Nachricht
operation = "Login|Client1|127.0.0.1|" + str(Client_Port_UDP) # Nickname, IP Adresse und UDP Port
# Packe die Anfrage-Nachricht als Bytes-Objekt
request = str.encode(operation)

#Anmelden beim Server
loggedin = False
while loggedin == False:
    server.send(request)
    ans = server.recv(1024)
    ansString = ans.decode('utf-8')
    if(ansString == 'Success'):
        loggedin = True
        print('logged in')

updates = threading.Thread(target=update).start()
chat = threading.Thread(target=listenchat).start()
tryConnectWithUser()

