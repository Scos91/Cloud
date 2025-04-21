import os
import time
import sys

def memory_exhaustion(num_forks, delay):
    print(f"[INFO] Starting memory exhaustion with up to {num_forks} forks and {delay}s delay between each...")

    forks = 0
    children = []
    try:
        for _ in range(num_forks):
            pid = os.fork()
            if pid == 0:
                while True:
                    pass #child persists indefinitely
            else:
                children.append(pid)
                forks += 1
                time.sleep(delay)
    except OSError as e:
        print(f"[ERROR] Fork limit reached or memory error: {e}")
    except KeyboardInterrupt:
        print("[INFO] Interrupted by user...")
    finally:
        print(f"[INFO] Total successful forks: {forks}")
        for pid in children:
            try:
                os.kill(pid, 9)
            except:
                continue

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 frkBombHost_Container.py <num_forks> <delay_in_seconds>")
        sys.exit(1)

    num_forks = int(sys.argv[1])
    delay = float(sys.argv[2])

    memory_exhaustion(num_forks, delay)