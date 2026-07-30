#!/usr/bin/env python3
# 📁 NodeHunter - Directory Finder v1.0
# By Nkwabena - Ghana 🇬🇭 | For ETHICAL / OWN sites only

import requests
import sys

print("📁 NodeHunter Directory Finder v1.0")
print("="*45)
print("⚠️  USE ONLY ON YOUR OWN SITES / WITH PERMISSION")
print("="*45)

target = input("Enter target URL (e.g., https://example.com): ").strip()
if not target.startswith("http"):
    target = "https://" + target
target = target.rstrip("/")

# Common paths - bug bounty starter list
wordlist = ["admin","login","dashboard","api","backup","config","test","dev","portal","wp-admin",".git",".env","robots.txt","sitemap.xml","uploads","images","js","css","backup.zip","old","beta"]

print(f"\n🚀 Scanning {target} for {len(wordlist)} paths...\n")

found = []
headers = {"User-Agent": "NodeHunter-Suite-Ethical-Scanner"}

for path in wordlist:
    url = f"{target}/{path}"
    try:
        r = requests.get(url, headers=headers, timeout=5, allow_redirects=False)
        code = r.status_code
        if code in [200, 301, 302, 403]:
            print(f"✅ [{code}] FOUND: {url}")
            found.append(f"[{code}] {url}")
        else:
            print(f"❌ [{code}] {url}")
    except Exception as e:
        print(f"⚠️  Error {url}: {e}")

print("\n" + "="*45)
print(f"🎯 Done! Found {len(found)} interesting paths")
for f in found:
    print(f)

# Save report
with open("directory_report.txt","w") as out:
    out.write("\n".join(found))
print("\n💾 Saved to directory_report.txt")
