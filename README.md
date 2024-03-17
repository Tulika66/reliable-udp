# reliableudp

Sender: Reads data from a file, constructs packets, sends them through the unreliable channel, and waits for ACKs. It uses a timer to handle timeouts and manages the sliding window.

Receiver: Listens for incoming packets, verifies checksums, sends ACKs for successfully received packets, and updates the base pointer.


Provides reliability over an unreliable UDP channel by implementing error detection (using checksums) and retransmission of lost packets (using acknowledgments and a sliding window mechanism).It employs a sliding window approach to send packets efficiently. It also handles acknowledgments (ACKs) received from the receiver, updating the base pointer, and managing the transmission window.
