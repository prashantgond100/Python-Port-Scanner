import socket
import argparse
import threading
from queue import Queue
import time

# A thread lock to prevent print statements from overlapping
print_lock = threading.Lock()

def scan_port(port, target_ip):
    """
    Attempts to connect to a specific port on the target IP.
    Returns True if the port is open, False otherwise.
    """
    try:
        # Create a new socket for each connection attempt
        # AF_INET = IPv4, SOCK_STREAM = TCP
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Set a short timeout to avoid long waits for closed ports
        s.settimeout(1)
        
        # Attempt to connect to the target
        con_result = s.connect_ex((target_ip, port))
        
        # A result of 0 means the connection was successful (port is open)
        if con_result == 0:
            with print_lock:
                print(f"[+] Port {port:<5} is OPEN")
            return True
        else:
            # Port is closed or filtered
            return False
            
    except Exception as e:
        # Handle potential errors during connection
        # print(f"Error scanning port {port}: {e}") # Uncomment for debugging
        return False
    finally:
        # Ensure the socket is always closed
        s.close()

def worker(q, target_ip):
    """
    Worker thread function.
    Pulls a port from the queue and scans it until the queue is empty.
    """
    while not q.empty():
        port = q.get()
        scan_port(port, target_ip)
        q.task_done()

def main(target, port_range, num_threads):
    """
    Main function to set up and run the port scanner.
    """
    print("-" * 50)
    print(f"Scanning target: {target}")
    print(f"Time started: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 50)
    
    try:
        target_ip = socket.gethostbyname(target)
        print(f"Resolved IP: {target_ip}\n")
    except socket.gaierror:
        print(f"[!] Error: Hostname '{target}' could not be resolved.")
        return

    # Create a queue to hold all the ports to be scanned
    q = Queue()
    for port in range(port_range[0], port_range[1] + 1):
        q.put(port)
        
    # Create and start the worker threads
    for _ in range(num_threads):
        thread = threading.Thread(target=worker, args=(q, target_ip))
        # Set as a daemon thread so it will exit when the main program exits
        thread.daemon = True
        thread.start()
        
    # Wait for all ports in the queue to be processed
    q.join()
    
    print("\n" + "-" * 50)
    print("Scan complete.")
    print("-" * 50)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A simple, multi-threaded Python port scanner.")
    
    parser.add_argument("target", help="The target IP address or hostname to scan.")
    parser.add_argument("-p", "--ports", dest="port_range", default="1-1024",
                        help="Port range to scan, e.g., '1-1024' or '80,443,8080'. Default is 1-1024.")
    parser.add_argument("-t", "--threads", dest="num_threads", type=int, default=50,
                        help="Number of threads to use for scanning. Default is 50.")

    args = parser.parse_args()

    # Parse the port range argument
    try:
        if ',' in args.port_range:
            # Handle comma-separated list of ports
            ports = [int(p.strip()) for p in args.port_range.split(',')]
            # For this simple implementation, we'll scan the range containing these ports
            start_port, end_port = min(ports), max(ports)
            # A more advanced version would scan only the specified ports
        else:
            # Handle range like '1-1024'
            start_port, end_port = map(int, args.port_range.split('-'))
        
        if not (1 <= start_port <= 65535 and 1 <= end_port <= 65535 and start_port <= end_port):
            raise ValueError()
            
    except ValueError:
        print("[!] Error: Invalid port range specified. Use format 'start-end' or 'p1,p2,...'.")
        exit()

    main(args.target, (start_port, end_port), args.num_threads)