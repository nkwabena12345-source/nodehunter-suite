import socket
from datetime import datetime

def scan(target, ports):
    print(f"\n--- Scanning {target} ---")
    print(f"Time: {datetime.now()}")
    print("-" * 40)
    open_ports = []
    
    for port in ports:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)  # 1 second
        result = sock.connect_ex((target, port))
        if result == 0:
            try:
                service = socket.getservbyport(port)
            except:
                service = "unknown"
            print(f"✅ Port {port} OPEN - {service}")
            open_ports.append(port)
        sock.close()
    
    print("-" * 40)
    if open_ports:
        print(f"Found {len(open_ports)} open ports: {open_ports}")
    else:
        print("No open ports in this range.")
    return open_ports

print("--- NODEHUNTER PORT SCANNER ---")
print("1. Scan your phone (localhost)")
print("2. Scan test server (scanme.nmap.org - legal to scan)")
print("3. Custom target (only your own!)")

choice = input("Choose 1/2/3: ")

if choice == "1":
    target = "127.0.0.1"
    ports = range(1, 1025)  # scan first 1024
    scan(target, ports)

elif choice == "2":
    target = "scanme.nmap.org"
    ports = [21,22,23,25,53,80,110,135,139,443,445,3306,8080]
    scan(target, ports)

elif choice == "3":
    target = input("Enter IP/domain YOU OWN: ")
    start = int(input("Start port: "))
    end = int(input("End port: "))
    scan(target, range(start, end+1))

else:
    print("Invalid choice")
