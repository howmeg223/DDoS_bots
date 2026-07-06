This document describes the setup for the isolated virtual lab used for this project. The aim of this setup is a fully contained environment for experimenting with DDoS attack techniques, detection and defence methods, with no risk of traffic leaking onto a real network.


There are four virtual machines on the isolated network:

testing-target -> the target machine (runs nginx) -> 192.168.168.10/24

testing-attacker -> attack machine (scapy, hping3) -> 192.168.168.11/24

testing-security -> monitoring machine -> 192.168.168.12/24

testing-reflector -> Open DNS machine / NTP reflector -> 192.168.168.13/24


All VMs run Ubuntu Server 24.04 LTS and do not have internet access.

Prequesites:
- VMware Workstation Pro (version 17)
- Ubuntu Server 24.04 LTS ISO
- Enable host machine with virtualisation in BIOS


Creating the Base VM:
1. In VMware Workstation Pro, select Create a New Virtual Machine
2. Create a typical setup and point it to the Ubuntu Server ISO
3. Name the VM and choose an appropriate storage location for all VM machines (they may take up around 20GB of storage)
4. Through the Ubuntu Server installer:
    - use the default storage layout
    - select none for Featured Server Snaps
    - ensure OpenSSH server is selected
5. Complete the install, and ensure the VM reboots cleanly
6. After booting, update the system:
    sudo apt update && sudo apt upgrade -y
7. Install the VM baseline tools:
    sudo apt install net-tools tcpdump curl -y
8. Take a snapshot of your base state (we are preserving the base VM before cloning):
    - Go to the VM tab
    - Go to Snapshot
    - Take Snapshot



Create the Isolated Network:
1. In VMware Workstation Pro, go to Edit, then Vitual Network Editor
2. Change Settings (you may need to get administrator access for windows)
3. Click Add Network and choose unused VMnet (VMnet2)
4. Set the type to Host Only (this keeps all traffic between the VMs and the host machine, with no internet access)
5. Note the assigned subnet (for this project we have 192.168.168.0/24)
6. Click Apply, then OK



Clone the Base VM:
Instead on installing the Ubuntu server on each VM, we clone the base VM to create each lab machine with the same base state.
1. Shut down the base VM:
    sudo shutdown now
2. In VMware, right-click the base VM, click manage, then clone.
3. Select "The current state in the virtual machine", then "Create a full clone"
4. Repeat the process to create four clones:
    - testing-target
    - testing-attacker
    - testing-security
    - testing-reflector



Configure Each Clone:
Each clone will inherit the hostname, machine ID, and SSH host keys from its base. If multiple VMs share these details, SSH identity conflixt and networking confusion may occur. Therefore, we configure each clone individually before use.

For each clone, perform the following steps:
1. Switch the network adapter to VMnet2:
As clones inherit the base Vm's NAT adapter, switching to VMnet2 places the Vm on the isolated lab network.
    - Shut down the VM if running
    - In VMware: right-click the VM, Settings, Network Adapter
    - Select Custom: Specific virtual network and choose VMnet2
    - Click OK
** Note: Some packages require internet access to install, for this you must switch temporarily back to NAT, install the required packages, then switch back to VMnet2. **

2. Set a unique hostname:
    sudo hostnamectl set-hostname testing-target
Verify this change using: hostnamectl (the prompt does not update until the next login)

3. Regenerate SSH host keys and machine ID:
Since clone share identical SSH host keys and machine IDs with the base image, we regenerate each VM a unique identity:
    sudo rm /etc/ssh/ssh_host_*
    sudo dpkg-reconfigure openssh-server
    sudo rm /etc/machine-id
    sudo systemd-machine-id-setup

4. Reboot the VM:
    sudo reboot
After rebooting, confirm the prompt shows the correct hostname



Assign Static IP Addresses:
Each VM receives a DHCP-assigned address on the 192.168.168.0/24 network by default. Since the attack script hardcode the IP addresses, each VM needs a permanent address that matches the scripts. 

- Edit the Netplan configuration file:
    sudo nano /etc/netplan/50-cloud-init.yaml

Then you must replace the contents of that file based on the VM:

testing-target (192.168.168.10):


    network:
        version: 2
        ethernets:
            ens33:
                dhcp4: false
                addresses: 
                    - 192.168.168.10/24
                routes:
                    - to: default
                    via: 192.168.168.1
                nameservers:
                    addresses: [192.168.168.1]


testing-attacker (192.168.168.11):


    network:
        version: 2
        ethernets:
            ens33:
                dhcp4: false
                addresses: 
                    - 192.168.168.11/24
                routes:
                    - to: default
                    via: 192.168.168.1
                nameservers:
                    addresses: [192.168.168.1]


testing-security (192.168.168.12):


    network:
        version: 2
        ethernets:
            ens33:
                dhcp4: false
                addresses: 
                    - 192.168.168.12/24
                routes:
                    - to: default
                    via: 192.168.168.1
                nameservers:
                    addresses: [192.168.168.1]
                    

testing-reflector (192.168.168.13):


    network:
        version: 2
        ethernets:
            ens33:
                dhcp4: false
                addresses: 
                    - 192.168.168.13/24
                routes:
                    - to: default
                    via: 192.168.168.1
                nameservers:
                    addresses: [192.168.168.1]        

** Note: the gateway address (192.168.168.1) is assigned by default for the Vmware DHCP service. You must confirm the correct value for your setup using ip route. **

To apply and verify the changes after configuring the netplan:
    sudo netplan apply
    ip a



Install Role-Specific Software:

For each Vm that needs packages:
1. Shut down VM
2. In VMware: VM Settings, Network Adapter, swutch to NAT
3. Power in the VM, then set Netplan back to DHCP:
    sudo nano /etc/netplan/50-cloud-init.yaml
    sudo netplan apply
    sudo reboot
4. Confirm the internet access using: ping -c 4 google.com
5. Install the required packages (see below)
6. Shut downm switch adapter back to Custom: VMnet2, restore the static Netplan config as shown in the Configure Clone section above, apply and reboot

testing-target:
    sudo apt update
    sudo apt install nginx -y
    sudo systemctl status nginx

testing-attacker:
    sudo apt update
    sudo apt install hping3 -y
    pip3 install scapy --break-system-packages

testing-security:
    sudo apt update
    sudo apt install wireshark tshark -y

testing-reflector:
    sudo apt update
    sudo apt install bind9 -y

- the BIND9 configuration is documented separately


Verify Connectivity:
confirm all VMs are reachable in the network

ping -c 192.168.168.10
ping -c 192.168.168.11
ping -c 192.168.168.12
ping -c 192.168.168.13

from testing-attacker, confirm that nginx is reachable on the target
curl http://192.168.168.10
- a successful response confirms end-to-end connectivity is working







