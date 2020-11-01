# Point-to-Multipoint-file-transfer-using-stop-and-wait-protocol
Client Side:
To send the file from client to servers, a user needs to the run the UDP_client.py python script in the following format:
python UDP_client.py <IP Address 1> <IP Address 2>...<IP Address n> <port no.> <File Name> <MSS>

eg: python UDP_client.py 10.154.11.49 152.14.142.133 152.14.142.24 7735 myfile 500

Server Side:
The server side script needs to be updated with the individual server’s IP address at UDP_IP_ADDRESS variable.
For allowing the servers to receive the file, a user needs to run the UDP_server.py python script in the following format:
python UDP_server.py <Port No.> <File Name> <Loss Probability>

eg: python UDP_server.py 7735 myfile 0.05

The inherent time out used in the client for waiting on ACK is 1 second.

Description:
Point-to-Multipoint File Transfer Protocol (P2MP-FTP)
The FTP protocol provides a sophisticated file transfer service, but since it uses TCP to ensure reliable data
transmission it only supports the transfer of files from one sender to one receiver. In many applications (e.g.,
software updates, stock quote updates, document sharing, etc) it is important to transfer data reliably from
one sender to multiple receivers. You will implement P2MP-FTP, a protocol that provides a simple service:
transferring a file from one host to multiple destinations. P2MP-FTP will use UDP to send packets from
the sending host to each of the destinations, hence it has to implement a reliable data transfer service using
some ARQ scheme; for this project, you will implement the Stop-and-Wait ARQ. Using the unreliable UDP
protocol allows us to implement a “transport layer” service such as reliable data transfer in user space.
Client-Server Architecture of P2MP-FTP
To keep things simple, you will implement P2MP-FTP in a client-server architecture and omit the steps
of opening up and terminating a connection. The P2MP-FTP client will play the role of the sender that
connects to a set of of P2MP-FTP servers that play the role of the receivers in the reliable data transfer.
All data transfer is from sender (client) to receivers (servers) only; only ACK packets travel from receivers
to sender.
Command Line Arguments
The P2MP-FTP server must be invoked as follows:
p2mpserver port# file-name p
where port# is the port number to which the server is listening (for this project, this port number is always
7735), file-name is the name of the file where the data will be written, and p is the packet loss probability
discussed above.
The P2MP-FTP client must be invoked as follows:
p2mpclient server-1 server-2 server-3 server-port# file-name MSS
where server-i is the host name where the i-th server (receiver) runs, i = 1, 2, 3, server-port# is the
port number of the server (i.e., 7735), file-name is the name of the file to be transferred, and MSS is the
maximum segment size.
