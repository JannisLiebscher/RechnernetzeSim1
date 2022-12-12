import socket
import struct
import threading

def handle_client(clinent_socket):
    run = True

    while run:
        # Empfange die Anfrage
        request = clinent_socket.recv(1024)

        size_id = struct.calcsize("!I")

        # Berechne die Größe des UTF-8-kodierten String-Teils der Anfrage-Nachricht
        size_operation = struct.calcsize("8s") + size_id

        # Berechne die Größe des Unsigned-Char-Wert-Teils der Anfrage-Nachricht
        size_n = struct.calcsize("B") + size_operation

        # Entpacke die Anfrage
        id = struct.unpack("!I", request[:size_id])[0]
        operation = struct.unpack("8s", request[size_id:size_operation])[0]
        n = struct.unpack("B", request[size_operation:size_n])[0]

        # Berechne die Größe des signed Integer-Teils der Anfrage-Nachricht
        size_numbers = n * 4
        numbers_raw = struct.unpack("%ds" % (n * 4), request[size_n:size_n + size_numbers])[0]

        # Konvertiere die Zahlen von signed Integers zu Python-Integern
        numbers = []
        for x in range(n):
            numbers.append(int.from_bytes(numbers_raw[x * 4: x * 4 + 4], "little"))

        # Führe die gewünschte Rechenoperation aus
        if operation == b"shutdown":
            # Schließe die Verbindung zum Client
            result=42
            result_bytes = result.to_bytes(4, "little")
            clinent_socket.sendall(struct.pack("!I", id) + result_bytes)
            run = False
            break
        if operation == b"Summe\x00\x00\x00":
            result = sum(numbers)
        elif operation == b"Produkt\x00":
            result = prod(numbers)
        elif operation == b"Minimum\x00":
            result = min(numbers)
        elif operation == b"Maximum\x00":
            result = max(numbers)

        # Packe das Ergebnis als signed Integer in ein Bytes-Objekt
        result_bytes = result.to_bytes(4, "little")
        # Sende das Ergebnis an den Client
        clinent_socket.sendall(struct.pack("!I", id) + result_bytes)


def prod(myList):
 
    # Multiply elements one by one
    result = 1
    for x in myList:
        result = result * x
    return result
# Erstelle einen TCP/IP-Socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Binde den Socket an eine Adresse und einen Port
print("Verbinde den Socket mit dem Server")
server_address = ('localhost', 5)
sock.bind(server_address)

# Lausche auf eingehende Verbindungen (maximal 1)
print("Horche auf Verbindung")
sock.listen(2)



while True:
    # Akzeptiere eine eingehende Verbindung
    print("Akzeptiere Verbindung")
    client_socket, client_address = sock.accept()
    client_thread = threading.Thread(target=handle_client, args=(client_socket,))
    client_thread.start()







