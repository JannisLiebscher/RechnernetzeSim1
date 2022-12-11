import socket
import struct

# Erstelle einen TCP/IP-Socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Verbinde den Socket mit dem Server
print("Verbinde den Socket mit dem Server")
server_address = ('localhost', 10000)
sock.connect(server_address)

# Erstelle die Anfrage-Nachricht
id = 1
operation = b"Summe"
n = 4
numbers = [3, 4, 10, 3]

# Packe die Zahlen als signed Integer in ein Bytes-Objekt
numbers_bytes = b"".join([number.to_bytes(4, "little") for number in numbers])

# Packe die Anfrage-Nachricht als Bytes-Objekt
request = struct.pack("!I8sB", id, operation, n) + numbers_bytes

# Sende die Anfrage an den Server
print("Sende die Anfrage an den Server")
sock.sendall(request)

# Empfange die Antwort vom Server
response = sock.recv(1024)

# Entpacke die Antwort
id, result = struct.unpack("!I4s", response)

# Konvertiere das Ergebnis von einem signed Integer in einen Python-Integer
result = int.from_bytes(result, "little")

# Gib das Ergebnis in der Konsole aus
print("ID:", id)
print("Ergebnis:", result)

# Schließe die Verbindung zum Server
sock.close()
