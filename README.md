Python Network Scanner

A simple, multi-threaded network port scanner built in Python. This tool allows you to scan a target IP address or hostname to identify open TCP ports.

This project was created to demonstrate proficiency in Python programming, socket programming fundamentals, and multi-threading for performance enhancement. It serves as a basic tool for network reconnaissance and educational purposes in cybersecurity.
<img width="2048" height="1500" alt="image" src="https://github.com/user-attachments/assets/5851e2cf-7ad8-450e-aa94-448b379880db" />
Features

Hostname Resolution: Automatically resolves hostnames to their corresponding IP addresses.

Flexible Port Specification: Scan a range of ports (e.g., 1-1024) or a specific, comma-separated list (e.g., 80,443,8080).

Multi-threading: Utilizes a thread pool to perform scans concurrently, significantly speeding up the process compared to a sequential scan.

Clean Output: Provides a clear and concise summary of open ports found.

How It Works

The script uses Python's built-in socket library to attempt TCP connections to the specified ports.

Socket Creation: For each port, a new socket object (AF_INET for IPv4, SOCK_STREAM for TCP) is created.

Connection Attempt: The socket.connect_ex() method is used. Unlike socket.connect(), this method returns an error code instead of raising an exception if a connection fails. A return code of 0 indicates a successful connection, meaning the port is open.

Threading & Queue: To manage concurrent scans, a Queue is populated with all the ports to be scanned. A pool of worker threads is created, each pulling a port from the queue and scanning it. This continues until the queue is empty.

Argument Parsing: The argparse library provides a clean command-line interface for specifying the target, ports, and number of threads.

Usage

Clone the repository:

git clone [https://github.com/your-username/python-network-scanner.git](https://github.com/your-username/python-network-scanner.git)
cd python-network-scanner


Run the script:

python port_scanner.py <target_ip_or_hostname> [options]


Examples

Scan a target for the default first 1024 ports:

python port_scanner.py 127.0.0.1


Scan a specific port range with 100 threads:

python port_scanner.py 192.168.1.1 -p 1-200 -t 100


Ethical Disclaimer

This tool is intended for educational purposes and for use in authorized security assessments. Never use this tool to scan networks or systems without explicit permission from the owner. Unauthorized scanning of networks is illegal and unethical. The author is not responsible for any misuse or damage caused by this program.
