import socket
import threading
import time

class PeerNode:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.peers = []

        # Start broadcasting thread
        threading.Thread(target=self.start_broadcasting, daemon=True).start()
        # Start listener for incoming broadcasts
        threading.Thread(target=self.listen_for_broadcasts, daemon=True).start()

        #threading.Thread(target=self.server_run, daemon=True).start()
        #threading.Thread(target=self.client_run, daemon=True).start()

    def start_broadcasting(self):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            
            s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            while True:
                message = f"NODE:{self.host}:{self.port}".encode()
                s.sendto(message, ('<broadcast>', 5000))  # Change 5000 to your chosen port
                time.sleep(5)  # Broadcast every 5 seconds

    def listen_for_broadcasts(self):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((self.host, 5000))  # Bind to the same port used for broadcasting
            while True:
                data, addr = s.recvfrom(1024)
                message = data.decode()
                if message.startswith("NODE:"):
                    _, peer_host, peer_port = message.split(":")
                    peer_info = (peer_host, int(peer_port))
                    if peer_info not in self.peers:
                        self.peers.append(peer_info)
                        print(f"Discovered peer: {peer_host}:{peer_port}")

    def connect_to_peer(self, peer_host, peer_port):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((peer_host, peer_port))
                s.sendall(b'Hello from node!')
                response = s.recv(1024)
                print(f"Response from {peer_host}:{peer_port} - {response.decode()}")
        except Exception as e:
            print(f"Failed to connect to {peer_host}:{peer_port} - {e}")

    '''def server_run():
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
        print(client.recv(1024))'''

    

if __name__ == "__main__":
    # Replace with your device's actual IP address
    node_host = '192.168.13.242'  # Device IP
    node_port = 5001  # Node port

    node = PeerNode(node_host, node_port)

    # Run indefinitely to keep the node alive
    while True:
        time.sleep(1)