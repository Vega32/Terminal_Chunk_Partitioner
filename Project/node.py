import socket
import threading

def server_run():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 5000))

    server.listen(4)

    while True:
        client, addr = server.accept()
        print(client.recv(1024).decode())
        client.send("Hello from server".encode())

def client_run():
    client=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('localhost', 5000))

    client.send('Hello from client'.encode())
    print(client.recv(1024))

threading.Thread(target=server_run).start()
client_thread=threading.Thread(target=client_run)

client_thread.start()