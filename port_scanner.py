#!/usr/bin/env python3
# NodeHunter Port Scanner - Ethical use only!
# Part of NodeHunter Security Suite v10.0

import socket
import threading
from datetime import datetime

COMMON_PORTS = {
    21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP",
    53: "DNS", 80: "HTTP", 110: "POP3", 135: "RPC",
    139: "NetBIOS", 143: "IMAP", 443: "HTTPS",
    445: "SMB", 993: "IMAPS", 995: "POP3S",
    1723: "PPTP", 3306: "MySQL", 3389: "RDP",
    5900: "VNC", 8080: "HTTP-Proxy"
}

open_ports = []

def scan_port(target, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        result = s.connect_ex((target, port))
        if result == 0:
            service = COMMON_PORTS.get(port, "Unknown")
            print(f"[OPEN] {port}/tcp - {service}")
            open_ports.append(port)
        s.close()
    except:
        pass

def main():
    target = input("Target IP/Domain: ").strip()
    print(f"\n[*] Scanning {target} - {datetime.now()}\n")
    
    threads = []
    for port in COMMON_PORTS:
        t = threading.Thread(target=scan_port, args=(target, port))
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()
    
    print(f"\n[+] Done! Found {len(open_ports)} open ports: {open_ports}")
    print("[*] Use only on systems you own/have permission to test!")

if __name__ == "__main__":
    main()0

