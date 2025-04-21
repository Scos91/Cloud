import multiprocessing
import time
import sys

def burn_cpu():
    while True:
        pass #for infinite loop

def cpuExhaustion(numProcesses, duration):
    try:
        print(f"[INFO] Starting CPU Exhaustion with {numProcesses} processes for {duration} seconds...")
        processes = []

        #start # of processes - numProcesses
        for _ in range(numProcesses):
            p = multiprocessing.Process(target=burn_cpu)
            p.start()
            processes.append(p)

        #run for duration
        time.sleep(duration)

        #terminate processes
        for p in processes:
            p.terminate()
            p.join()

        print("[INFO] CPU exhaustion attack completed.")
    except Exception as e:
        print(f"[ERROR] CPU exhaustion failed because: {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 burnCPU_VmHost.py <numProcesses> <duration>")
        sys.exit(1)

    numProcesses = int(sys.argv[1])
    duration = int(sys.argv[2])

    cpuExhaustion(numProcesses, duration)