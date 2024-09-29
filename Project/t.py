import threading
import time
import socket
def server_run():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 5000))

    server.listen(4)

    while True:
        client, addr = server.accept()
        time.sleep(10)
        print(client.recv(1024)=="Stop".encode())
        
        

def client_run():
    client=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('localhost', 5000))
    client.send("Stop".encode())

if __name__ == "__main__":
    threading.Thread(target=server_run).start()
    threading.Thread(target=client_run).start()