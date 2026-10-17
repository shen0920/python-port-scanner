import socket
import time

def scan_port(host, port, timeout=0.5):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.settimeout(timeout)
    try:
        result = client.connect_ex((host, port))
        return result == 0
    except socket.timeout:
        return False
    except OSError:
        return False
    finally:
        client.close()

def scan_range(host,start_port,end_port,timeout=0.5):
    open_ports = []
    for port in range(start_port, end_port + 1):
        if scan_port(host, port, timeout):
            open_ports.append(port)
    return open_ports

def main():
    host = "127.0.0.1"
    start_port = 1
    end_port = 60

    print(f"Scanning ports {start_port} to {end_port} on host {host}...")

    begin = time.perf_counter()
    open_ports = scan_range(host, start_port, end_port)
    cost = time.perf_counter() - begin

    print(f"Open ports: {open_ports}")
    print(f"Time taken: {cost:.2f} seconds")
    print(f"Total open ports: {len(open_ports)}")

if __name__ == "__main__":
    main()


