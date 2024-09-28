import socket
import threading
import FileManager
import os

class P2PNode:
    def __init__(self, host='0.0.0.0', port='12345'):
        self.host = host
        self.port = port
        self.peers = []

    def listen_for_connections(self):
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.bind((self.host, int(self.port)))
        listener.listen(5)
        print(f"Listening on {self.host}:{self.port}...")

        while True:
            client_socket, client_address = listener.accept()
            print(f"Connection from {client_address} established.")
            threading.Thread(target=self.handle_peer, args=(client_socket,)).start()

    def handle_peer(self, client_socket):
        while True:
            try:
                message = client_socket.recv(1024)
                if not message:
                    break
                print(f"Received: {message}")
                # Optionally, you could send an acknowledgment back
                client_socket.send(f"Echo: {message}")
            except ConnectionResetError:
                break
        client_socket.close()

    def connect_to_peer(self, peer_host, peer_port):
        peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            peer_socket.connect((peer_host, peer_port))
            self.peers.append(peer_socket)
            print(f"Connected to peer {peer_host}:{peer_port}")
        except Exception as e:
            print(f"Could not connect to {peer_host}:{peer_port}: {e}")

    def send_message_to_peer(self, message):
        for peer in self.peers:
            peer.send(message)

    def start(self):
        threading.Thread(target=self.listen_for_connections, daemon=True).start()
        while True:
            command = input("Enter a command (connect/send/exit): ")
            if command.startswith("connect"):
                _, host, port = command.split()
                self.connect_to_peer(host, int(port))
            elif command.startswith("send"):
                _, message = command.split(maxsplit=1)
                self.upload(message)
            elif command == "exit":
                break

    def upload(self, fileName):
        packets=FileManager.FileManager.divide_into_packets(fileName)
        for i in range (len(packets)):
            self.peers[i%len(self.peers)].send(packets[i])


    def download(self, file_name):
        
        pickle_files = []
        retrieved_packets = []
        ordered_packets = []
        for peer in self.peers:
            for file in os.listdir():
                if file.startswith(file_name) and file.endswith('.pkl'):
                    FileManager.FileManager.load_array_object_file(file)
                    pickle_files.append(retrieved_packets)
        
        count = 0
        while (count != retrieved_packets[0][4:7]):
            for packet in retrieved_packets:
                if (packet[:4] == count):
                    ordered_packets.append(packet)
                    count += 1

        if (FileManager.FileManager.reconstruct_file(ordered_packets, file_name)):
            print("Download Successful")
        else:
            print("Something went wrong when retrieving the file")


if __name__ == "__main__":
    port=input("Enter a Port: ")
    node = P2PNode('0.0.0.0', port)
    node.start()
