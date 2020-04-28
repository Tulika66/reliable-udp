import random
import socket
import time
import _thread
import hashlib



class packet:
    
    # checksum=0;
    
    # make packets in from byte data, and seqnum ->convert to sequence number
    @staticmethod
    def make_packet(sequence_num,data=b''):
        sequence_bytes=sequence_num.to_bytes(4,byteorder='little',signed=True)
        checksum = hashlib.md5(data).digest()
        return sequence_bytes + checksum + data
    
    
    
    @staticmethod
    def extract_packet(packet_fromfile):
        sequence_num=int.from_bytes(packet_fromfile[0:4],byteorder='little',signed=True)
        checksum_received = packet_fromfile[4:20]
        data_received = packet_fromfile[20:]
        checksum_created = hashlib.md5(data_received).digest()
        if(checksum_received==checksum_created):
            print("MD5 checksum verified")
        else:
            print("Packet is corrupted")
        return sequence_num, data_received
        
    
    
    @staticmethod    
    def make_empty_packet():
        return b''
  
        
   


class unreliable_channel :
    
    @staticmethod
    def send_pckt(packet,sock,addr):
        
        # if random.randint(0,chance)>0:
        sock.sendto(packet,addr)
        return
    
    
    @staticmethod
    def recv_pckt(sock):
        packet , addr=sock.recvfrom(1024)
        return packet , addr
        
        

class Timer(object):
    stop_time=-1
    
    def __init__(self,RTT_Time):
        self.start_time=self.stop_time
        self.duration=RTT_Time
        print("constructor finished")
        
    def start_timer(self):
        if(self.start_time==self.stop_time):
            self.start_time=time.time()
   
   
    def running(self):
       return self.start_time != self.stop_time
    
    def stop_timer(self):
        if(self.start_time != self.stop_time):
            self.start_time=self.stop_time
            
            
    def timeout(self):
        # if already stopped , ack recieved etc
        if not self.running():
            return False
        else :
            return time.time() - self.start_time >= self.duration
        


#constants declared
PACKET_SIZE= 512 #BYTES
RECEIVER_ADDRESS=('localhost',8080)
SENDER_ADDRESS=('localhost',0)
RTT=0.5
SLEEP_TIME=0.05
WINDOW=4
#shared resources
Base=0
lock=_thread.allocate_lock()
send_timer=Timer(RTT)


class reliable_layer :
    
    
    @staticmethod
    def give_window_size(total_packets):
        global Base
        if(WINDOW < total_packets - Base):
            return WINDOW
        else :
            return total_packets - Base
            
        
        
    @staticmethod
    def send(sock,packets_list): 
        global Base 
        global lock
        global send_timer
        
        
        total_packets= len(packets_list)
        window_size= reliable_layer.give_window_size(total_packets)
        print(' window size = ', window_size)       
        
        seq_no=0
        next_to_send=0
        base=0
        
        _thread.start_new_thread(reliable_layer.receive,(sock,))
        
        
        while Base < total_packets:
            lock.acquire()
            
            while( next_to_send < base + window_size):
                unreliable_channel.send_pckt(packets_list[next_to_send],sock,RECEIVER_ADDRESS)
                next_to_send+=1
                print('packet sent with number-: ',next_to_send-1,'\n')
                
            
            #start running timer,packet has been sent
            if not send_timer.running():
                send_timer.start_timer()
                print("timer started running\n")
            
            #wait until rtt timeout or ack received or stopped due to checksum
            while (send_timer.running() and not send_timer.timeout()):
                #release lock, somebody else can send packet
                lock.release()
                print("started sleeping\n")
                time.sleep(SLEEP_TIME)
                #enough sleep,start again
                lock.acquire()
                
            
            if send_timer.timeout():
                # all packets not send in current slot
                send_timer.stop_timer()
                next_to_send=Base
                print('timeout\n')
            
            else :
                #all pckets send in current window,succesfully
                window_size=reliable_layer.give_window_size(total_packets)
                print('shifting window\n')
            lock.release()
            
            
        unreliable_channel.send_pckt(packet.make_empty_packet(),sock,RECEIVER_ADDRESS)
        
            
                
    
    @staticmethod
    def receive (sock):
        global lock
        global Base
        global send_timer
        
        
        while True:
            
            packet_, addr= unreliable_channel.recv_pckt(sock)
            ack ,__= packet.extract(packet_)
            
            print("received ack - ",ack)
            
            if(ack >= Base):
                lock.acquire()
                base=ack+1
                print('base updated')
                send_timer.stop_timer()
                lock.release()
               
                        
         
        
        
        
        