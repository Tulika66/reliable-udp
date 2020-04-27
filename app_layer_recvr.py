import rudp
import socket
import sys


RECEIVER_ADDRESS= ('localhost',8080)

# def received_r(sock,filename):
print("eneter the filename to be written - :")
filename=input() 
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  
sock.bind(RECEIVER_ADDRESS)
file = open(filename,'wb')




expectednum=0
    
while True:
        packet,addr=rudp.unreliable_channel.recv_pckt(sock)
       
        if not packet:
            break
       
       
        recieved_seqnum,data=rudp.packet.extract_packet(packet)
        
    
        
        if(expectednum==recieved_seqnum):
            #send ack
            print("packet with seqnum received- ", recieved_seqnum)
            ack=rudp.packet.make_packet(recieved_seqnum)
            rudp.unreliable_channel.send_pckt(ack,sock,addr)
            expectednum+=1
            file.write(data)
        
        else :
            print('sending ack for expected-1 = ',expectednum-1,'\n')
            rollback_ack=rudp.packet.make_packet(expectednum-1)
            rudp.unreliable_channel.send_pckt(rollback_ack,sock,addr)
file.close()

sock.close()
    
            
           

    
