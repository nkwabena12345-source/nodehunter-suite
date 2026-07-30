import hashlib, socket, threading, os
from datetime import datetime
from queue import Queue

# --- FROM LEVEL 6 ---
def hash_pass(p): return hashlib.sha256(p.encode()).hexdigest()

def check_strength(p):
    score=0
    if len(p)>=8: score+=1
    if any(c.isupper() for c in p): score+=1
    if any(c.isdigit() for c in p): score+=1
    if any(c in "!@#$%^&*()" for c in p): score+=1
    return score

# --- FROM LEVEL 7 ---
def get_key(p): return hashlib.sha256(p.encode()).digest()
def encrypt_file(fname, pwd):
    key=get_key(pwd)
    with open(fname,"rb") as f: data=f.read()
    enc=bytes([data[i]^key[i%len(key)] for i in range(len(data))])
    with open(fname+".locked","wb") as f: f.write(enc)
    print(f"✅ Encrypted -> {fname}.locked")
def decrypt_file(fname, pwd):
    key=get_key(pwd)
    with open(fname,"rb") as f: data=f.read()
    dec=bytes([data[i]^key[i%len(key)] for i in range(len(data))])
    out=fname.replace(".locked",".unlocked")
    with open(out,"wb") as f: f.write(dec)
    print(f"✅ Decrypted -> {out}")

# --- FROM LEVEL 9 ---
def scan_port(target, port, results):
    try:
        s=socket.socket(); s.settimeout(1)
        if s.connect_ex((target,port))==0:
            try:
                s2=socket.socket(); s2.settimeout(2); s2.connect((target,port))
                banner=s2.recv(1024).decode(errors="ignore").strip()[:60]
                s2.close()
            except: banner="No banner"
            results.append((port,banner))
        s.close()
    except: pass

def fast_scan(target, ports):
    results=[]; q=Queue()
    for p in ports: q.put(p)
    def worker():
        while not q.empty():
            port=q.get(); scan_port(target,port,results); q.task_done()
    threads=[]
    for _ in range(50):
        t=threading.Thread(target=worker); t.daemon=True; t.start(); threads.append(t)
    q.join()
    return results


def subdomain_finder(domain):
    wordlist = ["www","mail","ftp","admin","blog","dev","test","api","vpn","shop","secure","portal","beta","demo","app","m"]
    print(f"\n🚀 Scanning {domain}...")
    found=[]
    for sub in wordlist:
        full = f"{sub}.{domain}"
        try:
            ip = socket.gethostbyname(full)
            print(f"✅ FOUND: {full} -> {ip}")
            found.append(full)
        except:
            print(f"❌ {full}")
    print(f"\n🎯 Found {len(found)} subdomains")
    return found


# --- MAIN SUITE ---
print("="*50)
print(" NODEHUNTER SECURITY SUITE v10.0 - FINAL BOSS")
print("="*50)

while True:
    print("\n1. Check password strength")
    print("2. Encrypt file")
    print("3. Decrypt file")
    print("4. Port scan")
    print("5. Full security audit + report")
    print("6. 🔍 Subdomain Finder [NEW]")
    print("7. Exit")
    c=input("Choose: ")

    if c=="1":
        p=input("Password: ")
        s=check_strength(p)
        print(f"Strength: {s}/4 | Hash: {hash_pass(p)[:20]}...")

    elif c=="2":
        f=input("File: "); pwd=input("Password: "); encrypt_file(f,pwd)
    elif c=="3":
        f=input("File.locked: "); pwd=input("Password: "); decrypt_file(f,pwd)
    elif c=="4":
        t=input("Target (127.0.0.1 or scanme.nmap.org): ")
        res=fast_scan(t, [21,22,80,443,3306,8080])
        for port,banner in res: print(f"✅ {port} -> {banner}")

    elif c=="5":
        print("\n--- RUNNING FULL AUDIT ---")
        target="scanme.nmap.org"
        res=fast_scan(target, [21,22,23,80,443,8080])
        with open("FINAL_REPORT.txt","w") as f:
            f.write(f"NODEHUNTER AUDIT {datetime.now()}\n")
            f.write(f"Target: {target}\nOpen ports:\n")
            for port,banner in res:
                f.write(f"- {port}: {banner}\n")
        print(f"Found {len(res)} open ports. Report saved to FINAL_REPORT.txt")
        print("AUDIT COMPLETE - YOU ARE A CYBER ENGINEER!")
    elif c=="6":
        d=input("Domain (e.g., google.com): ")
        subdomain_finder(d)
    elif c=="7": break
