# reliableudp

RUDP maintain a sliding window of transmitted but unacknowledged packets. 
The size of the sliding window is defined by RUDP_WINDOW. When the application provides RUDP with data to be 
sent, we determine whether any slots in the sliding window are open. If so, the 
packet can immediately be added to the window and transmitted. If not, we must 
queue the packet to be delivered once it can acquire a slot in the window.

Upon receiving an ACK packet, we inspect the first item in the sliding window. 
If the ACK packet is intended to acknowledge the first window item, we remove 
this item from the sliding window and shift any subsequent window items to the 
left, creating space in the window for new packets to be sent. As long as 
RUDP_WINDOW is greater than 1, this scheme provides better efficiency than 
stop-and-wait flow control by allowing up to RUDP_WINDOW outstanding 
unacknowledged packets to be sent.

When a non-ACK packet is sent in RUDP, a timer event is registered to occur 
after RUDP_TIMEOUT milliseconds. If the timeout event fires, the packet 
associated with it will be retransmitted, unless the packet has already been 
retransmitted RUDP_MAXRETRANS times, in which case we will trigger a 
RUDP_EVENT_TIMEOUT event.

When we receive an ACK, the timeout event for the packet being acknowledged is 
canceled. In RUDP, timeout events represent the detection of packet loss. Since 
we do not utilize negative acknowledgments, we instead detect packet loss 
implicitly when an ACK is not received.
