import rudp
import socket
import sys
import hashlib


RECEIVER_ADDRESS= ('localhost',8080)

# def received_r(sock,filename):
print("enter the filename to be written - :")
filename=input() 
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  
sock.bind(RECEIVER_ADDRESS)
file = open(filename,'wb')



expectednum=0
    
while True:
        packet,addr=rudp.unreliable_channel.recv_pckt(sock)
       
        if not packet:
            break
       
       
        recieved_seqnum,data_received=rudp.packet.extract_packet(packet)
        
        checksum = data_received[0:16]
        data = data_received[16:]
        checksum_created = hashlib.md5(data).digest()
                
        if(expectednum==recieved_seqnum and checksum==checksum_created):
            #send ack
            print("packet with seqnum received- ", recieved_seqnum)
            ack=rudp.packet.make_packet(recieved_seqnum)
            rudp.unreliable_channel.send_pckt(ack,sock,addr)
            expectednum+=1
            print(data)
            file.write(data)
        
        else :
            print('sending ack for expected-1 = ',expectednum-1,'\n')
            rollback_ack=rudp.packet.make_packet(expectednum-1)
            rudp.unreliable_channel.send_pckt(rollback_ack,sock,addr)
file.close()

sock.close()
print("Done")
    
            
           

    
