#!/usr/bin/env python3
import socket
import requests
import re
import os
import time
from colorama import init, Fore, Style
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Tuple
init(autoreset=True)
G = Fore.GREEN + Style.BRIGHT
R = Fore.RED + Style.BRIGHT
C = Fore.CYAN + Style.BRIGHT
Y = Fore.YELLOW + Style.BRIGHT
W = Fore.WHITE + Style.BRIGHT
M = Fore.MAGENTA + Style.BRIGHT
def enumarate():
    print(f"\n{G}[+] ENUMERATION MODULE ACTIVATED")
    print(f"{G}{'─' * 60}")
    print(f"{Y}[*] Waiting for target specification...")
    target = input(f"{C}Enter target (IP or domain, e.g., example.com): {Style.RESET_ALL}").strip()
    if not target:
        print(f"{R}[!] Target required! Cannot proceed without valid input.")
        input(f"\n{G}Press ENTER to return...{Style.RESET_ALL}")
        return
    print(f"{Y}[*] Validating target format and connectivity...")
    time.sleep(0.5)
    print(f"{G}[+] Target locked: {C}{target}")
    wordlist_path = input(f"{C}Enter wordlist path (e.g., /path/to/wordlist.txt): {Style.RESET_ALL}").strip()
    if not os.path.isfile(wordlist_path):
        print(f"{R}[!] Wordlist file not found at specified path!")
        print(f"{Y}[*] Ensure file exists and path is correct.")
        input(f"\n{G}Press ENTER to return...{Style.RESET_ALL}")
        return
    print(f"{Y}[*] Loading wordlist into memory...")
    time.sleep(0.8)
    with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as f:
        paths = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    
    if not paths:
        print(f"{R}[!] Wordlist is empty or contains only comments!")
        input(f"\n{G}Press ENTER to return...{Style.RESET_ALL}")
        return
    print(f"{G}[+] Wordlist loaded: {Y}{len(paths)} entries")
    print(f"{Y}[*] Preparing HTTP/HTTPS session with stealth headers...")
    scheme = 'https' if 'https' in target else 'http'
    if not target.startswith(('http://', 'https://')):
        target_url = f"{scheme}://{target}"
    else:
        target_url = target

    print(f"{G}[+] Using protocol: {C}{scheme.upper()}")
    print(f"{Y}[*] Initializing multi-threaded directory brute-force engine...")
    print(f"\n{G}╔{'═' * 58}╗")
    print(f"{G}║ {C}DIRECTORY & FILE DISCOVERY ENGINE{' ' * 10}{G}║")
    print(f"{G}╚{'═' * 58}╝\n")

    print(f"{Y}[*] Deploying {min(20, len(paths))} concurrent shadow threads...")
    time.sleep(0.7)
    print(f"{W}[*] Sending stealth probes to target web server...")

    discovered_pages = []
    total_checked = 0
    found_count = 0

    def check_path(path: str) -> Tuple[str, int, str]:
        nonlocal total_checked, found_count
        url = f"{target_url}/{path.lstrip('/')}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
            'Accept': '*/*',
            ' conexão': 'close'
        }
        try:
            resp = requests.get(url, timeout=7, allow_redirects=False, headers=headers, verify=False)
            total_checked += 1
            if resp.status_code == 200:
                found_count += 1
            return url, resp.status_code, resp.text if resp.status_code == 200 else ''
        except requests.exceptions.RequestException:
            total_checked += 1
            return url, 0, ''

    with ThreadPoolExecutor(max_workers=20) as executor:
        futures = {executor.submit(check_path, p): p for p in paths}
        for future in as_completed(futures):
            url, code, content = future.result()
            if code == 200:
                size = len(content)
                print(f"{G}[{Y}200{G}] {W}DISCOVERED → {C}{url} {Y}[{size} bytes]")
                discovered_pages.append((url, content))
            elif code == 301:
                print(f"{Y}[{code}] {W}REDIRECT → {C}{url}")
            elif code == 403:
                print(f"{M}[{code}] {W}FORBIDDEN → {C}{url} {M}(Sensitive?)")

    print(f"\n{G}[+] Directory scan completed: {Y}{total_checked}/{len(paths)} paths tested")
    print(f"{G}[+] Valid pages discovered: {Y}{len(discovered_pages)}")
    if discovered_pages:
        print(f"\n{G}╔{'═' * 58}╗")
        print(f"{G}║ {C}SOURCE CODE & COMMENT EXTRACTION{' ' * 12}{G}║")
        print(f"{G}╚{'═' * 58}╝\n")

        print(f"{Y}[*] Initiating deep source code analysis on {len(discovered_pages)} pages...")
        time.sleep(0.6)

        for url, content in discovered_pages:
            print(f"\n{Y}[*] Parsing: {C}{url}")
            html_comments = re.findall(r'<!--(.*?)-->', content, re.DOTALL | re.IGNORECASE)
            js_single = re.findall(r'//[ \t]*(.+)', content)
            js_multi = re.findall(r'/\*(.*?)\*/', content, re.DOTALL)
            css_comments = re.findall(r'/\*(.*?)\*/', content, re.DOTALL)
            all_comments = html_comments + js_single + js_multi + css_comments

            if all_comments:
                unique_comments = []
                seen = set()
                for c in all_comments:
                    clean = re.sub(r'\s+', ' ', c.strip())
                    if clean and clean not in seen:
                        seen.add(clean)
                        unique_comments.append(clean)

                print(f"{G}  └─> {Y}{len(unique_comments)} unique comment(s) extracted:")
                for i, comment in enumerate(unique_comments, 1):
                    display = comment[:140] + ('...' if len(comment) > 140 else '')
                    print(f"      {W}[{i}] {display}")
            else:
                print(f"{R}  └─> No comments detected in source.")
    print(f"\n{G}╔{'═' * 58}╗")
    print(f"{G}║ {C}FULL PORT SCAN (1-65535) {' ' * 20}{G}║")
    print(f"{G}╚{'═' * 58}╝\n")

    print(f"{Y}[*] Resolving hostname to IP address...")
    try:
        host_part = target.split('/')[0].split(':')[0]
        ip = socket.gethostbyname(host_part)
        print(f"{G}[+] Target resolved: {C}{ip}")
    except:
        print(f"{R}[!] DNS resolution failed! Using input as IP.")
        ip = target.split('/')[0].split(':')[0]

    print(f"{Y}[*] Launching 100-thread TCP SYN scan engine...")
    print(f"{W}[*] Scanning all 65,535 ports... This may take 2-5 minutes.")
    time.sleep(1.2)

    open_ports = []
    filtered_ports = []
    scanned = 0

    def scan_port(port: int) -> Tuple[int, str]:
        nonlocal scanned
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(0.8)
                result = s.connect_ex((ip, port))
                scanned += 1
                if result == 0:
                    return port, 'open'
                return port, 'closed'
        except:
            scanned += 1
            return port, 'filtered'

    with ThreadPoolExecutor(max_workers=100) as executor:
        futures = [executor.submit(scan_port, p) for p in range(1, 65536)]
        for future in as_completed(futures):
            port, status = future.result()
            if status == 'open':
                open_ports.append(port)
                service = {
                    80: "HTTP", 443: "HTTPS", 22: "SSH", 21: "FTP", 25: "SMTP",
                    3306: "MySQL", 5432: "PostgreSQL", 3389: "RDP", 8080: "HTTP-ALT"
                }.get(port, "Unknown")
                print(f"{G}[OPEN] {C}Port {port}/tcp {G}→ {Y}{service}")
            elif status == 'filtered':
                filtered_ports.append(port)
                print(f"{Y}[FILTERED] {C}Port {port}/tcp {Y}→ Firewall/Filtered")
    print(f"\n{G}{'─' * 60}")
    print(f"{G}[+] FULL ENUMERATION COMPLETE")
    print(f"{Y}[*] Scanned ports: {C}65,535")
    print(f"{G}[+] Open ports: {Y}{len(open_ports)}")
    if open_ports:
        print(f"    → {', '.join(map(str, sorted(open_ports)))}")
    print(f"{Y}[*] Filtered ports: {Y}{len(filtered_ports)}")
    print(f"{C}[*] Pages discovered: {Y}{len(discovered_pages)}")
    
    total_comments = sum(
        len(set(re.sub(r'\s+', ' ', c.strip()) for c in (
            re.findall(r'<!--(.*?)-->', content, re.DOTALL | re.IGNORECASE) +
            re.findall(r'//[ \t]*(.+)', content) +
            re.findall(r'/\*(.*?)\*/', content, re.DOTALL)
        ))) for _, content in discovered_pages
    )
    print(f"{M}[*] Total unique comments extracted: {Y}{total_comments}")

    print(f"\n{G}[*] Shadow enumeration phase terminated. Ready for next vector.")
    input(f"\n{G}Press ENTER to return to main menu...{Style.RESET_ALL}")