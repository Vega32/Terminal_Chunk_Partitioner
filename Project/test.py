import socket
import threading
import FileManager
import os
import struct

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
        packet_per_peer=[]
        
        while True:
            try:
                message = client_socket.recv(1024)
                if not message:
                    break
                if(message=="Stop".encode()):
                    print("\nEntered if\n")
                    

                    h=FileManager.FileManager.HEADER_SIZE
                    unpacked_header = struct.unpack(FileManager.FileManager.HEADER_FORMAT, packet_per_peer[0][:h])
                    file_name = unpacked_header[2].decode().strip()

                    print(file_name)
                    FileManager.FileManager.store_array_object_file(packet_per_peer, f"{file_name.replace('\0','')}_{self.host}_{self.port}")
                    print("\nFile Created\n")
                else:
                    packet_per_peer.append(message)
                #print(f"Received: {message}")
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
            elif command.startswith("get"):
                _, message = command.split(maxsplit=1)
                self.download(message)
            elif command == "exit":
                break

    def upload(self, fileName):
        packets=FileManager.FileManager.divide_into_packets(fileName)
        for i in range (len(packets)):
            self.peers[i%len(self.peers)].send(packets[i])
        for j in range (len(self.peers)):
            self.peers[j].send("Stop".encode())


    def download(self, file_name):
        
        unpacked_header=[]
        retrieved_packets = []
        ordered_packets = []
        for peer in self.peers:
            for file in os.listdir():
                if file.startswith(file_name) and file.endswith('.pkl'):
                    retrieved_packets.append(FileManager.FileManager.load_array_object_file(file))
        count = 0

        h=FileManager.FileManager.HEADER_SIZE
        print(retrieved_packets[0][:h])
        unpacked_header = struct.unpack(FileManager.FileManager.HEADER_FORMAT, retrieved_packets[0][:h])
        nb_packets = unpacked_header[1].decode().strip()

        while (count <= nb_packets):
            for packet in retrieved_packets:

                unpacked_header = struct.unpack(FileManager.FileManager.HEADER_FORMAT, retrieved_packets[0][:h])
                id = unpacked_header[0].decode().strip()

                if (id == count):
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
