#!/usr/bin/env python3
import subprocess
import csv
import sys

DOMAINS = ["google.com", "github.com", "ya.ru"]
OUTPUT_CSV = "dns_traceroute.csv"

def get_ip(domain):
    try:
        res = subprocess.run(
            ["dig", "+short", domain],
            capture_output=True, text=True, timeout=5
        )
        ips = [ip.strip() for ip in res.stdout.splitlines() if ip.strip()]
        for ip in ips:
            if "." in ip:
                return ip
        return ips[0] if ips else "NO_IP"
    except Exception:
        return "DNS_FAILED"

def run_traceroute(ip):
    if ip in ("DNS_FAILED", "NO_IP"):
        return "SKIPPED"
    try:
        res = subprocess.run(
            ["traceroute", "-n", "-m", "15", "-w", "2", ip],
            capture_output=True, text=True, timeout=30
        )
        return res.stdout.strip().replace("\n", " | ")
    except subprocess.TimeoutExpired:
        return "TRACEROUTE_TIMEOUT"
    except FileNotFoundError:
        return "ERROR: traceroute not installed"
    except Exception as e:
        return f"ERROR: {e}"

def main():
    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Domain", "IP_Address", "Traceroute_Output"])
        
        for domain in DOMAINS:
            ip = get_ip(domain)
            print(f"IP: {ip}", end=" | ")
            trace = run_traceroute(ip)
            writer.writerow([domain, ip, trace])
            
if __name__ == "__main__":
    main()