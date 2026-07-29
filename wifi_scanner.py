#!/usr/bin/env python3
# NodeHunter WiFi Scanner LITE - No API needed!
import subprocess, re

print("="*50)
print(" NodeHunter WiFi Scanner LITE")
print("="*50)

try:
    print("\n[*] Your Current WiFi:")
    out = subprocess.run(["ip","a"], capture_output=True, text=True).stdout
    print(out)
    print("\n[*] Nearby WiFi via dumpsys:")
    try:
        scan = subprocess.run(["dumpsys","wifi"], capture_output=True, text=True, timeout=5).stdout
        ssids = re.findall(r'SSID: "(.*?)"', scan)
        if ssids:
            print(f"[+] Found {len(set(ssids))} networks:")
            for s in set(ssids):
                if s: print(f" - {s}")
        else:
            print("[!] Android blocked scan (needs API)")
    except Exception as e:
        print(e)
except Exception as e:
    print(f"Error: {e}")
print("\n[+] Done!")
