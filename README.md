# Terminal Chunk Partitioner
## 💡 Inspiration
- Networking is a vital area of computer science, and through this project, we wanted to explore this field, more specifically how systems communicate using TCP/IP, while addressing challenges like data transmission and reliability.
- We set out to build a distributed Peer-to-Peer (P2P) system capable of splitting large files into manageable chunks for seamless sharing between at least 4 devices.
- Our goal was to develop a straightforward, reliable system using the TCP/IP protocol to ensure error-free file transfers.

## 🚀 What it does
- 🗂️ Splits files into chunks with a maximum size of 512 bytes and distributes them across a network of at least 4 nodes.
- ⬆️ Uploads and ⬇️ downloads file chunks between nodes.
- 🛠️ Reconstructs the original file with complete integrity after all chunks are collected.
- ✅ Verifies the correctness of the downloaded file once all chunks have been received and assembled.

## 🛠️ How we built it
- Leveraged the **socket** library to implement TCP/IP networking, establishing continuous communication between the nodes.
- If a node wants to upload a file, it is divided into 512-byte chunks, each starting with a custom header, which are then distributed and transferred across the nodes.
- If that node wants to retrieve its original file, it retrieves the different packets from the nodes it was spread to, reconstructs them in order, and saves it as a new file.
- The system was built in **Python**, focusing on efficient chunking, network transfer, and file reconstruction, ensuring reliability throughout the process.

## ⚠️ Challenges we ran into 
- Learning how to effectively use the **socket**, **threading**, and **struct** libraries for building the system.
- Maintaining **file integrity** during chunking, transmission, and reconstruction was a significant challenge.
- Solving issues related to properly **reconstructing the original file** from distributed chunks.
- Handling **slicing and processing headers** during file transfer.
- Designing a mechanism to prevent peers from unnecessarily waiting for packets after the file transfer is completed.
- Managing **concurrent transfers** across multiple nodes while handling network errors such as packet loss or connection drops.

## 🎉Accomplishments that we're proud of
- Successfully established a functional network with more than 4 nodes capable of **reliable upload and download** of file chunks.
- Achieved **file integrity** and ensured smooth reconstruction of the original file after transfers.
- Built a fully operational P2P file-sharing system from the ground up using the TCP/IP stack.
- Our system can handle **files of any extension** and reliably reconstructs them after transfer.

## 📚What we learned
- Enhanced our understanding of **socket programming** and the intricacies of the **TCP/IP networking stack**.
- Developed skills to handle **distributed data transfers** and ensure data integrity in networked environments.
- Gained valuable experience in managing **concurrent communication** between multiple nodes in a P2P system.

## ⏩ What's next for Terminal Chunk Partitioner
- Implement **encryption** for secure file transfers, ensuring data confidentiality. 🔒
- Handling nodes joining and leaving the network without compromising data
- Introduce recovery mechanisms for **handling interrupted transfers** to improve reliability.
- Optimize the algorithm for the downloading logic, reducing the complexity and enhancing performance.

