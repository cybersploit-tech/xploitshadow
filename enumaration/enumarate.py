from utils.animation import loading_animation
from utils.ColorsX import Colors
import socket
import threading
import time
import queue
import requests
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

# Disable SSL warnings
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

class PortScanner:
    def __init__(self, target):
        self.target = target.strip()
        self.open_ports = []
        self.lock = threading.Lock()
        self.common_ports = {
            21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS",
            80: "HTTP", 110: "POP3", 143: "IMAP", 443: "HTTPS", 445: "SMB",
            3389: "RDP", 3306: "MySQL", 5432: "PostgreSQL", 5900: "VNC",
            8080: "HTTP-Proxy", 8443: "HTTPS-Alt", 27017: "MongoDB",
            6379: "Redis", 1433: "MSSQL", 1521: "Oracle", 5000: "Flask/Docker",
            9200: "Elasticsearch", 11211: "Memcached", 25565: "Minecraft", 10000: "Webmin"
        }
        self.http_ports = [80, 443, 8080, 8443, 8000, 5000, 3000, 8081, 8082, 8083, 8008, 8089]

    def resolve_target(self):
        try:
            ip = socket.gethostbyname(self.target)
            print(f"{Colors.GREEN}[+] Target resolved: {Colors.CYAN}{self.target}{Colors.RESET} -> {Colors.CYAN}{ip}{Colors.RESET}")
            return ip
        except socket.gaierror:
            print(f"{Colors.RED}[-] Cannot resolve hostname: {self.target}")
            return None

    def get_service_name(self, port):
        try:
            return socket.getservbyport(port)
        except:
            return self.common_ports.get(port, "unknown")

    # FIXED BANNER GRABBING (now works for SSH, FTP, SMTP, MySQL, etc.)
    def grab_banner(self, ip, port):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(4)
            sock.connect((ip, port))

            banner = ""
            if port == 22:  # SSH
                sock.send(b"\n")
                banner = sock.recv(1024).decode(errors='ignore')
            elif port == 21:  # FTP
                banner = sock.recv(1024).decode(errors='ignore')
            elif port == 25 or port == 587:  # SMTP
                banner = sock.recv(1024).decode(errors='ignore')
            elif port == 3306:  # MySQL
                banner = sock.recv(1024).hex()[:100]
            elif port in self.http_ports:  # HTTP/S
                request = f"GET / HTTP/1.0\r\nHost: {self.target}\r\n\r\n"
                sock.send(request.encode())
                banner = sock.recv(2048).decode(errors='ignore')
            else:
                sock.send(b"\r\n")
                banner = sock.recv(1024).decode(errors='ignore')

            sock.close()
            return banner.strip().replace("\n", " ").replace("\r", " ")[:120]
        except:
            return "No banner"

    def scan_port(self, ip, port):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.6)
            result = sock.connect_ex((ip, port))
            sock.close()
            if result == 0:
                service = self.get_service_name(port)
                banner = self.grab_banner(ip, port)
                with self.lock:
                    self.open_ports.append({'port': port, 'service': service, 'banner': banner})
                print(f"\r{Colors.GREEN}[+] {port}/tcp OPEN -> {Colors.YELLOW}{service:<12}{Colors.RESET} {Colors.WHITE}{banner[:60]}{Colors.RESET}" + " " * 10)
                return True
        except:
            pass
        return False

    def scan_all_ports(self, ip, max_workers=800):
        print(f"\n{Colors.CYAN}[*] Starting full port scan (1-65535)...")
        print(f"{Colors.CYAN}[*] Using {max_workers} threads\n")
        start_time = time.time()
        total = 65535
        scanned = 0
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {executor.submit(self.scan_port, ip, port): port for port in range(1, 65536)}
            for future in as_completed(futures):
                scanned += 1
                if scanned % 1500 == 0 or scanned == total:
                    elapsed = time.time() - start_time
                    speed = scanned / elapsed if elapsed > 0 else 0
                    eta = (total - scanned) / speed if speed > 0 else 0
                    print(f"\r{Colors.MAGENTA}[*] {scanned}/{total} | {speed:.0f} p/s | ETA: {eta:.1f}s      ", end="", flush=True)
        print()
        return time.time() - start_time

    def print_results(self, elapsed):
        print(f"\n{Colors.GREEN}{'=' * 88}")
        print(f"{Colors.BOLD}{Colors.CYAN}               PORT SCAN RESULTS - {self.target.upper()}")
        print(f"{Colors.GREEN}{'=' * 88}")
        print(f"{Colors.CYAN}[i] Time: {Colors.YELLOW}{elapsed:.2f}s ({elapsed/60:.1f} min) | Open: {Colors.GREEN}{len(self.open_ports)}{Colors.RESET}\n")
        if self.open_ports:
            print(f"{Colors.GREEN} {'PORT':<6} {'SERVICE':<15} {'BANNER'}")
            print(f"{'-' * 88}")
            for item in sorted(self.open_ports, key=lambda x: x['port']):
                b = item['banner'] if item['banner'] != "No banner" else ""
                print(f"{Colors.CYAN}{item['port']:<6}{Colors.RESET} {Colors.YELLOW}{item['service']:<15}{Colors.RESET} {Colors.WHITE}{b}{Colors.RESET}")
        else:
            print(f"{Colors.RED}[-] No open ports detected.")
        print(f"{Colors.GREEN}{'=' * 88}\n")


class DirectoryBruter:
    def __init__(self, target, port, wordlist_path):
        self.target = target
        self.port = port
        self.scheme = "https" if port in [443, 8443] else "http"
        self.base_url = f"{self.scheme}://{self.target}" + (f":{port}" if port not in [80, 443] else "")
        self.wordlist_path = wordlist_path
        self.wordlist = self.load_wordlist()
        self.found_dirs = set()
        self.found_files = set()
        self.queue = queue.Queue()
        self.lock = threading.Lock()

    def load_wordlist(self):
        if not os.path.isfile(self.wordlist_path):
            print(f"{Colors.RED}[-] Wordlist not found: {self.wordlist_path}")
            return None
        try:
            with open(self.wordlist_path, "r", encoding="utf-8") as f:
                words = [line.strip() for line in f if line.strip() and not line.startswith("#")]
            print(f"{Colors.GREEN}[+] Loaded wordlist: {Colors.YELLOW}{len(words):,} words{Colors.RESET} from {Colors.CYAN}{self.wordlist_path}")
            return words
        except Exception as e:
            print(f"{Colors.RED}[-] Failed to load wordlist: {e}")
            return None

    def check_path(self, path):
        if not path or path == "/":
            return False
        url = f"{self.base_url}{path}".replace("//", "/")
        try:
            r = requests.get(url, timeout=7, allow_redirects=True, verify=False, headers={"User-Agent": "Mozilla/5.0"})
            if r.status_code in [200, 301, 302, 401, 403]:
                size = len(r.content)
                print(f"{Colors.GREEN}[+] {r.status_code} {Colors.WHITE}{url} {Colors.CYAN}[{size} bytes]{Colors.RESET}")
                if path.endswith("/"):
                    with self.lock:
                        if url not in self.found_dirs:
                            self.found_dirs.add(url)
                            self.queue.put(path.rstrip("/"))
                else:
                    with self.lock:
                        self.found_files.add(url)
                return True
        except:
            pass
        return False

    def brute_once(self, base=""):
        if not self.wordlist:
            return
        paths = []
        prefix = "/" + base if base and not base.startswith("/") else base
        prefix = prefix + "/" if prefix and not prefix.endswith("/") else prefix

        for word in self.wordlist:
            paths.append(prefix + word)
            paths.append(prefix + word + "/")
            paths.append(prefix + word + ".php")
            paths.append(prefix + word + ".html")

        with ThreadPoolExecutor(max_workers=100) as executor:
            for path in paths:
                if path != "/" and path:
                    executor.submit(self.check_path, path)

    def recursive_brute(self):
        if not self.wordlist:
            return
        print(f"\n{Colors.CYAN}[*] Starting recursive brute force -> {Colors.YELLOW}{self.base_url}/")
        self.queue.put("")
        depth = 0
        while not self.queue.empty() and depth < 4:
            current = self.queue.get()
            print(f"{Colors.MAGENTA}[*] Depth {depth} -> /{current}/")
            self.brute_once(current)
            depth += 1

        total = len(self.found_dirs) + len(self.found_files)
        print(f"\n{Colors.GREEN}{'=' * 88}")
        print(f"{Colors.BOLD}{Colors.CYAN}       BRUTE FORCE COMPLETE -> {self.base_url}")
        print(f"{Colors.GREEN}{'=' * 88}")
        if total == 0:
            print(f"{Colors.RED}[-] No directories or files discovered.")
        else:
            if self.found_dirs:
                print(f"{Colors.CYAN}[+] {len(self.found_dirs)} Directories:")
                for d in sorted(self.found_dirs)[:30]:
                    print(f"    {Colors.GREEN}+ {d}")
            if self.found_files:
                print(f"{Colors.CYAN}[+] {len(self.found_files)} Files:")
                for f in sorted(self.found_files)[:25]:
                    print(f"    {Colors.GREEN}+ {f}")
        print(f"{Colors.GREEN}{'=' * 88}\n")


def port_scan():
    print(f"\n{Colors.CYAN}{Colors.BOLD}╔═══════════════════════════════════════════════════════════════╗")
    print(f"{Colors.CYAN}{Colors.BOLD}║             ULTIMATE SCANNER v6.0 - FIXED & FASTER            ║")
    print(f"{Colors.CYAN}{Colors.BOLD}╚═══════════════════════════════════════════════════════════════╝\n")

    target = input(f"{Colors.GREEN}[?] Target (domain/IP): {Colors.WHITE}").strip()
    if not target:
        print(f"{Colors.RED}[-] Target required!")
        return

    print(f"\n{Colors.MAGENTA}[?] Wordlist path (e.g. wordlist.txt):")
    wordlist = input(f"{Colors.GREEN} └─> {Colors.WHITE}").strip() or "wordlist.txt"
    if not os.path.isfile(wordlist):
        print(f"{Colors.RED}[-] File not found: {wordlist}")
        input(f"{Colors.YELLOW}Press Enter to exit...")
        return

    scanner = PortScanner(target)
    loading_animation("[*] Resolving target...")
    ip = scanner.resolve_target()
    if not ip:
        return

    loading_animation("[*] Scanning all 65535 ports...")
    elapsed = scanner.scan_all_ports(ip)
    scanner.print_results(elapsed)

    http_ports = [p['port'] for p in scanner.open_ports if p['port'] in scanner.http_ports]
    if http_ports:
        print(f"{Colors.MAGENTA}[+] Web ports open: {Colors.YELLOW}{http_ports}")
        for port in http_ports:
            loading_animation(f"[*] Brute forcing {target}:{port} ...")
            bruter = DirectoryBruter(target, port, wordlist)
            bruter.recursive_brute()
    else:
        print(f"{Colors.YELLOW}[i] No web ports -> skipping brute force.")

    input(f"\n{Colors.YELLOW}Done! Press Enter to exit...")


if __name__ == "__main__":
    port_scan()