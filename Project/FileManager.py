import os
import struct
import hashlib
import pickle

class FileManager:
    PACKET_SIZE = 512  # 512 Byte chunks
    HEADER_FORMAT = 'I I 32s 32s' # packet id, total packets, file name, checksum, total of 102 Byte
    HEADER_SIZE = struct.calcsize(HEADER_FORMAT)

    # calculate checksum to check correctness of file
    @staticmethod
    def calculate_checksum(data_chunk):
        return hashlib.md5(data_chunk).hexdigest().encode('utf-8')

    # add header to packet
    @staticmethod
    def create_header(string_format, packet_id, nb_packets, file_name, checksum):
        return struct.pack(
            FileManager.HEADER_FORMAT,
            packet_id,
            nb_packets,
            file_name[:32],
            checksum[:32]
        )

    # divide original file in 512 Byte maximum sized chunks
    @staticmethod
    def divide_into_packets(file_path):
        packets = []

        packet_id = 0
        file_name = os.path.basename(file_path).encode('utf-8')
        file_full_size = os.path.getsize(file_path)
        nb_packets = (file_full_size + FileManager.PACKET_SIZE -1) // FileManager.PACKET_SIZE
        
        # packet creation
        with open(file_path, 'rb') as file:
            while True:

                data_chunk = file.read(FileManager.PACKET_SIZE)
                if not data_chunk:
                    break
            
                checksum = FileManager.calculate_checksum(data_chunk)
                header = FileManager.create_header(FileManager.HEADER_FORMAT, packet_id, nb_packets, file_name, checksum)

                packet = header + data_chunk
                packets.append(packet)

                packet_id += 1
        file.close()
        return packets

    # retrieve different packets to form the original file
    @staticmethod
    def reconstruct_file(packets, new_file_name):
        with open(new_file_name, 'wb') as file:
            count =0
            for packet in packets:
                data_chunk = packet[FileManager.HEADER_SIZE:]

                unpacked_header = struct.unpack(FileManager.HEADER_FORMAT, packet[:FileManager.HEADER_SIZE])
                retrieved_checksum = unpacked_header[3].decode().strip()
                expected_checksum = FileManager.calculate_checksum(data_chunk)

                # checking reliability using the checksum
                if unpacked_header[3] != expected_checksum:
                    print(f"Checksum mismatch for packet ID {unpacked_header[count]}. Expected: {expected_checksum}, Actual: {retrieved_checksum}")
                    return False
                
                file.write(data_chunk)
                count += 1
        file.close()
        return True

    #Store array of packets as object file
    @staticmethod
    def store_array_object_file(packets, file_name):
        if os.path.exists(file_name):
            os.remove(file_name)
        with open(file_name + '.pkl', 'wb') as file:
            pickle.dump(packets, file)
        file.close()
    
    #Store array of packets as object file
    @staticmethod
    def load_array_object_file(pickle_file_name):
        with open(pickle_file_name, 'rb') as file:
            loaded_packets = pickle.load(file)
        file.close()
        
        return loaded_packets

    '''def main():
        # Example file path
        file_path = "images.jpg"  # Replace with your file path
        
        # Divide the file into packets
        packets = divide_into_packets(file_path)
        
        # Example: Print packet details
        for i, packet in enumerate(packets):
            header = packet[:HEADER_SIZE]
            data_chunk = packet[HEADER_SIZE:]
            unpacked_header = struct.unpack(HEADER_FORMAT, header)
            
            print(f"Packet {i}:")
            print(f"Header - Packet Number: {unpacked_header[0]}, Total Chunks: {unpacked_header[1]}, File Name: {unpacked_header[2].decode().strip()}")
            print(f"Data Chunk Size: {len(data_chunk)} bytes")
            print(f"Content of chunk: {data_chunk}")

        if (reconstruct_file(packets, "images.png")):
            print("Success!!")

if __name__ == "__main__":
    main()'''

