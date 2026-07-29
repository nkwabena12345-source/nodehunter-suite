import socket
import threading
from datetime import datetime
from queue import Queue

print_lock = threading.Lock()
open_ports = []

def grab_banner(target, port):
    try:
        s = socket.socket()
        s.settimeout(2)
        s.connect((target, port))
        # try to get banner
        try:
            banner = s.recv(1024).decode().strip()
        except:
            banner = "No banner"
        s.close()
        return banner
    except:
        return "No banner"

def scan_port(target, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    result = sock.connect_ex((target, port))
    if result == 0:
        banner = grab_banner(target, port)
        try:
            service = socket.getservbyport(port)
        except:
            service = "unknown"
        with print_lock:
            print(f"✅ {port:5} OPEN | {service:12} | {banner[:50]}")
            open_ports.append((port, service, banner))
    sock.close()

def threaded_scan(target, ports, threads=100):
    print(f"\n--- NODEHUNTER PRO SCANNER ---")
    print(f"Target: {target}")
    print(f"Ports: {len(ports)} | Threads: {threads}")
    print(f"Time: {datetime.now()}")
    print("-" * 60)
    
    q = Queue()
    for p in ports:
        q.put(p)
    
    def worker():
        while not q.empty():
            port = q.get()
            scan_port(target, port)
            q.task_done()
    
    thread_list = []
    for _ in range(threads):
        t = threading.Thread(target=worker)
        t.daemon = True
        t.start()
        thread_list.append(t)
    
    q.join()
    print("-" * 60)
    print(f"DONE. Found {len(open_ports)} open ports.")
    
    # save report
    with open(f"scan_{target}_{datetime.now().strftime('%H%M')}.txt", "w") as f:
        f.write(f"Scan report for {target} at {datetime.now()}\n")
        for port, service, banner in open_ports:
            f.write(f"{port} - {service} - {banner}\n")
    print(f"Report saved!")

while True:
    print("\n1. Fast scan phone (1-1024)")
    print("2. Fast scan scanme.nmap.org")
    print("3. Custom")
    print("4. Exit")
    c = input("Choose: ")
    
    open_ports.clear()
    
    if c == "1":
        threaded_scan("127.0.0.1", range(1, 1025))
    elif c == "2":
        common = [21,22,23,25,53,80,110,135,139,143,443,445,993,995,1723,3306,3389,5900,8080,8443]
        threaded_scan("scanme.nmap.org", common)
    elif c == "3":
        t = input("Target YOU OWN: ")
        s = int(input("Start port: "))
        e = int(input("End port: "))
        threaded_scan(t, range(s, e+1))
    elif c == "4":
        break
