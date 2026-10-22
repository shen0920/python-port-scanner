import socket
import time
import argparse
from concurrent.futures import ThreadPoolExecutor

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

def scan_range(host,start_port,end_port,timeout=0.5,workers=200):
    ports = range(start_port,end_port + 1)
    with ThreadPoolExecutor(max_workers = workers) as pool:
        results = pool.map(lambda port: (port, scan_port(host, port,timeout)),ports)
    return sorted(port for port, is_open in results if is_open)

def parse_args():
    parser = argparse.ArgumentParser(description= "简单的TCP端口扫描器")
    parser.add_argument("host", help="目标主机")
    parser.add_argument("start_port", type=int, help="起始端口" )
    parser.add_argument("end_port", type=int, help="结束端口")
    parser.add_argument("--timeout", type=float, default=0.5, help="连接超时时间（秒）")
    parser.add_argument("--workers", type=int, default=200, help="并发线程数")
    return parser.parse_args()

def validate(args):
    if not(1 <= args.start_port <= 65535):
        raise SystemExit("起始端口必须在1到65535之间")
    if not(1 <= args.end_port <= 65535):
        raise SystemExit("结束端口必须在1到65535之间")
    if args.start_port > args.end_port:
        raise SystemExit("起始端口不能大于结束端口")

def main():
    args = parse_args()
    validate(args)

    print(f"Scanning ports {args.start_port} to {args.end_port} on host {args.host}...")

    begin = time.perf_counter()
    open_ports = scan_range(args.host, args.start_port, args.end_port, args.timeout, args.workers)
    cost = time.perf_counter() - begin

    print(f"Open ports: {open_ports}")
    print(f"Time taken: {cost:.2f} seconds")
    print(f"Total open ports: {len(open_ports)}")

if __name__ == "__main__":
    main()
