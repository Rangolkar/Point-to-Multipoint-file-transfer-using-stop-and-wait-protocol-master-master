import socket
import sys
import struct
import random
import datetime

def calculate_checksum(s): #calculate the checksum of received data
	return '%4X' % (-(sum(ord(c) for c in s) % 65536) & 0xFFFF)

def verify_checksum(s): #checks if the calculated checksum and the checksum received in the header is same
	a=s[3].decode()
	return int(bin(int(calculate_checksum(a), 16))[2:], 2) == s[1]

def recv_data(UDP_PORT_NO,UDP_IP_ADDRESS,filename,probablity):
	header_len=8
	serverSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	serverSock.bind((UDP_IP_ADDRESS, int(UDP_PORT_NO)))
	print("\nSERVER IS LISTENING........\n")
	start_time1=datetime.datetime.now()
	end_time1=datetime.datetime.now()
	start_time=end_time1-start_time1
	print("START TIME: ",start_time)
	current_seq=1
	while True:
		raw_data, addr = serverSock.recvfrom(1024)
		n = len(raw_data) - header_len
		data = struct.unpack('iHH' + str(n) + 's', raw_data)
		m=verify_checksum(data)
		if m==True:	
			sequence_num=data[0]
			rcvd_msg=data[3]
			r=random.random()
			if r>=float(probablity): #if the random number generated is less than the probablity ACK packet is sent  
				#if sequence_num==current_seq: #checks if the sequence number of the received packet is in order
				ack_num=sequence_num
				current_seq=current_seq+1
				with open(filename+".txt","ab") as f: #saves the received data in a file
					f.write(rcvd_msg)
				#else:
				#ack_num=current_seq
				field=0b0000000000000000
				field1=0b1010101010101010
				print("\nPacket RECEIVED\n")
				print("Details of the received packet are:") #printing the details of the received packet
				print("Sequence Number: ",data[0])
				print("Checksum: ",bin(data[1])[2:])
				print("Field value: ",bin(data[2])[2:])
				a=struct.pack('iHH' , ack_num, field, field1)
				#print("\nMessage: ",rcvd_msg)
				serverSock.sendto(a, (addr[0], addr[1]))
				if data[2]==43691:
					end_time=datetime.datetime.now()
					total_time=end_time-start_time1
					print("TOTAL TIME: ",total_time)
					serverSock.close()
					break
			else:
				print("\nPacket LOST\n")
				print("Details of the lost packet are:")
				print("Sequence Number: ",data[0])
				print("Checksum: ",bin(data[1])[2:])
				print("Field value: ",bin(data[2])[2:])


def main(argv):
	probablity=argv[-1]
	filename=argv[-2]
	UDP_PORT_NO=argv[-3]
	UDP_IP_ADDRESS = "127.0.0.1" #ip address of the server machine will change for every host machine
	recv_data(UDP_PORT_NO,UDP_IP_ADDRESS,filename,probablity)

	
	    
if __name__ == "__main__":
    main(sys.argv[1:])
