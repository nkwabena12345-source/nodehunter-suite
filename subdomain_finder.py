#!/usr/bin/env python3
# 🔍 NodeHunter - Subdomain Finder v1.0
# By Nkwabena - Ghana 🇬🇭

import socket
import sys

print("🔍 NodeHunter Subdomain Finder v1.0")
print("="*40)

target = input("Enter domain (e.g., google.com): ").strip()
if not target:
    print("❌ No domain entered!")
    sys.exit()

# Common subdomains list
wordlist = ["www", "mail", "ftp", "admin", "blog", "dev", "test", "api", "vpn", "shop", "secure", "portal", "beta", "demo", "stage", "app", "m", "mobile", "support", "help", "docs"]

print(f"\n🚀 Scanning {target} for {len(wordlist)} subdomains...\n")

found = []
for sub in wordlist:
    domain = f"{sub}.{target}"
    try:
        ip = socket.gethostbyname(domain)
        print(f"✅ FOUND: {domain} -> {ip}")
        found.append(f"{domain} -> {ip}")
    except:
        print(f"❌ Not found: {domain}")

print("\n" + "="*40)
print(f"🎯 Done! Found {len(found)} subdomains")
if found:
    print("\n".join(found))
