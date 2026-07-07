Developing and Defending DDoS Attacks at Packet-Level:

This project is a self-directed cybersecurity research project that aims to explore how 
Distributed Denial-of-Service (DDoS) attacks work at packet-level. 
These attacks are created using python and the library Scapy, and are launched in an isolated lab environment.
The attacks are then monitored, analysed and defended against.

Research Overview:
This project is inspired by the TryHackMe Detecting DDoS room: https://tryhackme.com/room/detectingwebddos
It aims to develop an understanding of how these attacks work at the network and application layers. 
In order to build meaningful defences again DDoS attacks, you must first understand the attack mechanics.

This poses the research question:
How do common DDoS attack types behave at the packet level, and what charactistics in their traffic patterns can 
be used to develop effective detection and defence mechanisms?

The scope of this project:
- Building and understanding direct DDoS attack scripts
- Building reflection/amplification attacks
- Setting up a fully isolated lab environment across four VMs
- Capturing and analysing attack traffic from a monitoring VM
- Developing detection logic and defence techniques based on the observed traffic patterns

It is not intended for real-world exploitation of networks or systems outside the isolated lab.


Future Development:
A planned extension of this project is the development of machine learning for anomaly detection trained on the 
traffic captured in this lab and determining if a supervised model can reliably distinguished attack traffic to normal traffic. 

Lab Environment:
All attacks and defences are developed and launched in the fully isolated VMware lab environment
with no internet access, ensuring there is no risk of traffic leaking onto a real network.

testing-target -> 192.168.168.10 -> Target Machine (nginx web werver)
testing-attacker -> 192.168.168.11 -> Attacker Machine (Scapy, hping3)
testing-security -> 192.168.168.12 -> Monitoring and investigation machine (Wireshark, tcpdump)
testing-reflector -> 192.168.168.13 -> Open DNS Machine / NTP reflector for amplification attacks

Attack Scripts:
The attack scripts are written in Python using Scapy for raw packet crafting, except for Slowloris which requires Python's standard socket library.
All scripts are documented with notes of protocol mechanics included.


Direct Attacks:
These are attacks that are send directly from the attacker to the victim.

scripts/direct/syn_flood.py -> SYN flood -> using TCP -> exhausts the targets connection table with half-open connections

scripts/direct/udp_flood.py -> UDP flood -> using UDP -> overwhelms the target with max-size UDP packets

scripts/direct/icmp_flood.py -> ICMP flood -> using ICMP -> overwhelms the target with echo request packets

scripts/direct/tcp_rst.py -> TCP RST Hijack -> using TCP -> Hijacks RST packets to terminate an already existing connection

scripts/direct/slowloris.py -> Slowloris -> HTTP / TCP -> exhausts the server connection pool with incomplete HTTP requests


Reflection / Amplification attacks:
These attacks use a third-party reflector to send attack traffic to the victim using IP spoofing.

scripts/reflection/icmp_reflection.py -> SMURF -> using ICMP -> echo replies directed at the spoofed target address

scripts/reflection/udp_ntp.py -> NTP ampification -> using UDP / NTP -> using monlist command responses

scripts/reflection/dns_amplification.py -> DNS amplification -> using UDP / DNS -> large txt responses directed at the spoofed target address


Project Structure:

├── README.md
├── docs/
│   ├── lab-setup.md           # Full VM and network setup guide
│   └── theory.md              # Attack theory and protocol mechanics 
├── scripts/
│   ├── direct/                 # Direct attack scripts
│   └── reflection/             # Reflection/amplification attack scripts
└── results/                    # Packet captures, observations, and findings





