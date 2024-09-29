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
        #print(f"Listening on {self.host}:{self.port}...")

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
                    if packet_per_peer!=[]:

                        h=FileManager.FileManager.HEADER_SIZE
                        unpacked_header = struct.unpack(FileManager.FileManager.HEADER_FORMAT, packet_per_peer[0][:h])
                        file_name = unpacked_header[2].decode().strip()

                        FileManager.FileManager.store_array_object_file(packet_per_peer, f"{file_name.replace('\0','')}_{self.host}_{self.port}")
                        print("\nFile Created\n")
                else:
                    packet_per_peer.append(message)
            except ConnectionResetError:
                break
        client_socket.close()

    def connect_to_peer(self, peer_host, peer_port):
        peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            peer_socket.connect((peer_host, peer_port))
            self.peers.append(peer_socket)
            print(f"\nConnected to peer {peer_host}:{peer_port}\n")
        except Exception as e:
            print(f"\nCould not connect to {peer_host}:{peer_port}: {e}\n")

    def send_message_to_peer(self, message):
        for peer in self.peers:
            peer.send(message)

    def printMenu(self):
        print("\n-----------------------------Terminal Chunk Partitioner-----------------------------------\n")
        print("Commands:\n")
        print("connect [IP] [Port]")
        print("send [File Path]")
        print("get [File Name] [New File Name]")
        print("help")
        print("exit\n")

    def start(self):
        threading.Thread(target=self.listen_for_connections, daemon=True).start()
        self.printMenu()
        while True:
            
            command = input("Enter a command: ")
            if command.startswith("connect"):
                _, host, port = command.split()
                self.connect_to_peer(host, int(port))
            elif command.startswith("send"):
                _, message = command.split(maxsplit=1)
                self.upload(message)
            elif command.startswith("get"):
                _, message, new_file_name = command.split(maxsplit=2)
                self.download(message, new_file_name)
            elif command == "exit":
                break
            elif command == "help":
                self.printMenu()

    def upload(self, fileName):
        packets=FileManager.FileManager.divide_into_packets(fileName)
        for i in range (len(packets)):
            self.peers[i%len(self.peers)].send(packets[i])
        for j in range (len(self.peers)):
            self.peers[j].send("Stop".encode())


    def download(self, file_name, new_file_name):
        
        retrieved_pickle_files = []
        unpacked_header=[]
        ordered_packets = []
        for peer in self.peers:
            for file in os.listdir():
                if file.startswith(file_name) and file.endswith('.pkl'):
                    retrieved_pickle_files.append(FileManager.FileManager.load_array_object_file(file))
        count = 0
        
        h=FileManager.FileManager.HEADER_SIZE
        unpacked_header = struct.unpack(FileManager.FileManager.HEADER_FORMAT, retrieved_pickle_files[0][0][:h])
        nb_packets = unpacked_header[1]

        while (count < nb_packets):
            for retrieved_packet_list in retrieved_pickle_files:
                for packet in retrieved_packet_list:
                    unpacked_header = struct.unpack(FileManager.FileManager.HEADER_FORMAT, packet[:h])
                    id = unpacked_header[0]

                    if (id == count):
                        ordered_packets.append(packet)
                        count += 1

        if (FileManager.FileManager.reconstruct_file(ordered_packets, new_file_name)):
            print("Download Successful")
        else:
            print("Something went wrong when retrieving the file")

    


if __name__ == "__main__":
    host=input("Enter an IP: ")
    port=input("Enter a Port: ")
    node = P2PNode(host, port)
    node.start()
