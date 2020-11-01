import socket
import sys
import threading
import struct
import datetime
import time

def server_info(ip_addr):
	global server_address
	server_address[ip_addr]={}
	server_address[ip_addr]['timeout']=0
	server_address[ip_addr]['ack_rcvd']=False

def Connection(address,port,sequence_num):
	global ACK
	global server_address
	global data
	global ACK
	global server_address_list
	global timeout
	global field
	timeout=2
	ACK=0
	for j in range (0,len(data)):
		a=data[j].decode('utf-8')
		checksum1=checksum_func(a) #executes checksum of the MSS size of data
		checksum=int(bin(int(checksum1, 16))[2:], 2)
		currentsegdone=False
		while currentsegdone == False: #executes stop and wait protocol that is the client waits till it has not received the ACKs from all the server
			a=len(server_address_list)
			currentsegdone=stopandwait(a,j)
		sequence_num=sequence_num+1 #increments sequence number for every MSS byte of data
		if sequence_num==len(data):
			field=0b01010101010101011
		clientSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		clientSock.setblocking(0)
		a=struct.pack('iHH' + str(len(data[j])) + 's', sequence_num, checksum, field, data[j]) #packs the header and data to be sent in a structure
		server_address[address]['ack_rcvd']=False #initially no acknowldment is received from any receiver hence the ack_received field is false
		server_address[address]['timeout']=0 #before sending data timeout is set to 0
		while server_address[address]['ack_rcvd']==False:
			clientSock.sendto(a, (address,int(port)))
			start_timeout=time.time() #starting timeout
			while True:
				try:
					msg, addr = clientSock.recvfrom(1024)
					server_address[address]['ack_rcvd']=True
					recv_data = struct.unpack('iHH' , msg)
					ack_no=recv_data[0]
					print("\nAcknowledgment received from ",address) #printing the details of the acknowldment received from receivers
					print("Acknowledgment number: ",ack_no)
					print("Acknowledgment packet field: ",bin(recv_data[2])[2:])
					if sequence_num==recv_data[0]:
						ACK=ACK+1 #on receiving acknowledment the ACK flag is incremented by 1
					break
				except BlockingIOError:
					end_timeout=time.time()
					server_address[address]['timeout'] = end_timeout - start_timeout #if timeout occurs the loop is broken and and the packet is send again
					if(server_address[address]['timeout']>1):
						break
					else:
						pass

def stopandwait(expectedACK,j): #waits till the the client has not received acknowledment from all the receivers 
	global ACK
	if ACK>=(expectedACK*j):
		return True
	return False

def checksum_func(s):
	return '%4X' % (-(sum(ord(c) for c in s) % 65536) & 0xFFFF)  #executes checksum of the data

def rdt_send():
	global ACK
	global server_address_list
	global server_address
	global UDP_PORT_NO
	global sequence_num
	global data
	sequence_num=0
	Thread_list=[]
	time_start=datetime.datetime.now()
	print("START TIME: ",time_start)
	for i in range (len(server_address_list)): #starts thread for different servers who will receive the data
		MainThread = threading.Thread(target=Connection,args=(server_address_list[i],UDP_PORT_NO,sequence_num))
		MainThread.start()
		Thread_list.append(MainThread)
	for thread in Thread_list:
		thread.join()
	time_end=datetime.datetime.now()
	time_exec=time_end-time_start
	print("TOTAL TIME: ",time_exec) #prints the time required for the entire process 

def main(argv):
	global ACK
	global server_address
	global server_address_list
	global UDP_PORT_NO
	global sequence_num
	global data
	server_address={}
	MSS=argv[-1] #Takes the value of MSS, filename, port number and the server address from the argument
	file_name=argv[-2]
	with open(file_name+".txt","rb") as f: #divides the entire file in the MSS bytes of data and stores it in a list data
		while f.read(1):
			byte=f.read(int(MSS))
			data.append(byte)
	UDP_PORT_NO=argv[-3]
	server_address_list=argv[:-3]
	for i in range (len(server_address_list)): #saves the ip address of all the servers in a list
		server_info(server_address_list[i])
	rdt_send() #calls rdt send to send the MSS to each server
	

if __name__ == "__main__":
	data=[]
	UDP_PORT_NO=0
	MSS=0
	file_name=''
	global field
	field=0b01010101010101010
	global ACK
	ACK=0
	main(sys.argv[1:])
