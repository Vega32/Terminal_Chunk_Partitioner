import os
import struct
import hashlib

PACKET_SIZE = 512  # 512 Byte chunks
HEADER_FORMAT = 'I I 32s 32s' # packet id, total packets, file name, checksum, total of 102 Byte
HEADER_SIZE = struct.calcsize(HEADER_FORMAT)

# calculate checksum to check correctness of file
def calculate_checksum(data_chunk):
    return hashlib.md5(data_chunk).hexdigest().encode('utf-8')

# add header to packet
def create_header(string_format, packet_id, nb_packets, file_name, checksum):
    return struct.pack(
        HEADER_FORMAT,
        packet_id,
        nb_packets,
        file_name[:32],
        checksum[:32]
    )

# divide original file in 512 Byte maximum sized chunks
def divide_into_packets(file_path):
    packets = []

    packet_id = 0
    file_name = os.path.basename(file_path).encode('utf-8')
    file_full_size = os.path.getsize(file_path)
    nb_packets = (file_full_size + PACKET_SIZE -1) // PACKET_SIZE
    
    # packet creation
    with open(file, 'rb') as file:
        while True:

            data_chunk = file.read(PACKET_SIZE)
            if (data_chunk == NULL):
                break
            
            checksum = calculate_checksum(data_chunk)
            header = create_header(HEADER_FORMAT, packet_id, nb_packets, file_name, checksum)

            packet = header + data_chunk
            packets.append(packet)

            packet_id += 1

    return packets

# retrieve different packets to form the original file
def reconstruct_file(packets, file_name, nb_packets):
    return null

def main():
    # Example file path
    file_path = "example.txt"  # Replace with your file path
    
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

if __name__ == "__main__":
    main()

