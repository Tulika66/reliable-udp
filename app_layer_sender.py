import rudp
import socket
import _thread
import time


PACKET_SIZE=512

filename=  input ('filename')

sock= socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
     
#     try :s
file = open(filename, 'rb')
#     except IOError:
#          print("unable to open file ")
       
        
        
packets=[]
sequence_num=0
while True:
          data =file.read(PACKET_SIZE)
          if not data:
              break
          packets.append(rudp.packet.make_packet(sequence_num,data))     
          sequence_num+=1
          
total_packets=len(packets)
rudp.reliable_layer.send(sock,packets)
sock.close()
    
        



