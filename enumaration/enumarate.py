from utils.animation import loading_animation
from utils.ColorsX import Colors
import socket
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

class PortScanner:
    def __init__(self, target):
        self.target = target
        self.open_ports = []
        self.closed_ports = []
        self.filtered_ports = []
        self.lock = threading.Lock()
        
        self.common_ports = {
            21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP",
            53: "DNS", 80: "HTTP", 110: "POP3", 143: "IMAP",
            443: "HTTPS", 445: "SMB", 3306: "MySQL", 3389: "RDP",
            5432: "PostgreSQL", 5900: "VNC", 8080: "HTTP-Proxy",
            8443: "HTTPS-Alt", 27017: "MongoDB", 6379: "Redis",
            1433: "MSSQL", 5000: "Flask", 8000: "Django", 465: "SMTPS",
            587: "SMTP", 993: "IMAPS", 995: "POP3S", 3000: "Node.js",
            5001: "Docker", 9000: "PHP-FPM", 9090: "Prometheus", 
            50000: "SAP", 8888: "Jupyter", 10000: "Webmin"
        }
    
    def resolve_target(self):
        try:
            ip = socket.gethostbyname(self.target)
            print(f"{Colors.GREEN}[+]{Colors.RESET} Target resolved: {Colors.CYAN}{self.target}{Colors.RESET} -> {Colors.CYAN}{ip}{Colors.RESET}")
            return ip
        except socket.gaierror:
            print(f"{Colors.RED}[!]{Colors.RESET} Cannot resolve target: {self.target}")
            return None
    
    def scan_port(self, ip, port, timeout=0.5):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            result = sock.connect_ex((ip, port))
            
            if result == 0:
                try:
                    service = socket.getservbyport(port)
                except:
                    service = self.common_ports.get(port, "Unknown")
                
                banner = self.grab_banner(sock, port)
                
                with self.lock:
                    self.open_ports.append({
                        'port': port,
                        'service': service,
                        'banner': banner,
                        'state': 'OPEN'
                    })
                    print(f"\r{Colors.GREEN}[+]{Colors.RESET} Found open port: {Colors.CYAN}{port}{Colors.RESET} ({Colors.YELLOW}{service}{Colors.RESET})" + " "*20)
                
                sock.close()
                return True
            else:
                with self.lock:
                    self.closed_ports.append(port)
                sock.close()
                return False
                
        except socket.timeout:
            with self.lock:
                self.filtered_ports.append(port)
            return False
        except Exception as e:
            return False
    
    def grab_banner(self, sock, port):
        try:
            if port in [80, 8080, 8000]:
                sock.send(b"GET / HTTP/1.1\r\nHost: target\r\n\r\n")
            elif port == 21:
                pass
            elif port == 22:
                pass 
            else:
                sock.send(b"\r\n")
            sock.settimeout(1)
            banner = sock.recv(1024).decode('utf-8', errors='ignore').strip()
            return banner[:100] if banner else "No banner"
        except:
            return "No banner"
    def scan_all_ports(self, ip, threads=300):
        print(f"\n{Colors.CYAN}[*]{Colors.RESET} Scanning ALL ports (1-65535)...")
        print(f"{Colors.CYAN}[*]{Colors.RESET} Using {threads} threads")
        print(f"{Colors.YELLOW}[*]{Colors.RESET} This may take 10-20 minutes...\n")
        start_time = time.time()
        total_ports = 65535
        scanned = 0
        with ThreadPoolExecutor(max_workers=threads) as executor:
            futures = {executor.submit(self.scan_port, ip, port): port 
                      for port in range(1, 65536)}
            for future in as_completed(futures):
                scanned += 1
                if scanned % 500 == 0:
                    progress = (scanned / total_ports) * 100
                    elapsed = time.time() - start_time
                    rate = scanned / elapsed if elapsed > 0 else 0
                    eta = (total_ports - scanned) / rate if rate > 0 else 0
                    print(f"\r{Colors.YELLOW}[*]{Colors.RESET} Progress: {progress:.1f}% ({scanned}/{total_ports}) | "
                          f"Speed: {rate:.0f} ports/s | ETA: {eta/60:.1f}m", end='', flush=True)
        print()
        end_time = time.time()
        elapsed = end_time - start_time  
        return elapsed
    def print_results(self, elapsed_time):
        print(f"\n{Colors.GREEN}{'='*80}{Colors.RESET}")
        print(f"{Colors.CYAN}{Colors.BOLD}                         FULL SCAN RESULTS{Colors.RESET}")
        print(f"{Colors.GREEN}{'='*80}{Colors.RESET}\n")
        print(f"{Colors.CYAN}[i]{Colors.RESET} Target: {Colors.YELLOW}{self.target}{Colors.RESET}")
        print(f"{Colors.CYAN}[i]{Colors.RESET} Total Ports Scanned: {Colors.YELLOW}65535{Colors.RESET}")
        print(f"{Colors.CYAN}[i]{Colors.RESET} Scan Duration: {Colors.YELLOW}{elapsed_time:.2f}s ({elapsed_time/60:.1f} minutes){Colors.RESET}")
        print(f"{Colors.CYAN}[i]{Colors.RESET} Open Ports Found: {Colors.GREEN}{len(self.open_ports)}{Colors.RESET}")
        print(f"{Colors.CYAN}[i]{Colors.RESET} Closed Ports: {Colors.RED}{len(self.closed_ports)}{Colors.RESET}")
        print(f"{Colors.CYAN}[i]{Colors.RESET} Filtered Ports: {Colors.YELLOW}{len(self.filtered_ports)}{Colors.RESET}\n")
        if self.open_ports:
            print(f"{Colors.GREEN}{'='*80}{Colors.RESET}")
            print(f"{Colors.GREEN}{Colors.BOLD}                         OPEN PORTS DETAILS{Colors.RESET}")
            print(f"{Colors.GREEN}{'='*80}{Colors.RESET}\n")
            print(f"    {'PORT':<10} {'STATE':<10} {'SERVICE':<20} {'BANNER':<35}")
            print(f"    {'-'*80}")
            
            for port_info in sorted(self.open_ports, key=lambda x: x['port']):
                port = port_info['port']
                state = port_info['state']
                service = port_info['service']
                banner = port_info['banner'][:35]             
                print(f"    {Colors.CYAN}{port:<10}{Colors.RESET} "
                      f"{Colors.GREEN}{state:<10}{Colors.RESET} "
                      f"{Colors.YELLOW}{service:<20}{Colors.RESET} "
                      f"{banner:<35}")          
            print(f"\n{Colors.GREEN}{'='*80}{Colors.RESET}")
        else:
            print(f"{Colors.RED}[!]{Colors.RESET} No open ports found")
            print(f"\n{Colors.GREEN}{'='*80}{Colors.RESET}")
        print(f"\n{Colors.CYAN}[*]{Colors.RESET} Scan completed successfully!")
        print(f"{Colors.CYAN}[*]{Colors.RESET} Results are displayed above\n")
def port_scan():
    print(f"\n{Colors.CYAN}{Colors.BOLD}╔════════════════════════════════════════════════════════╗{Colors.RESET}")
    print(f"{Colors.CYAN}{Colors.BOLD}║              FULL ENUMARATION SCANNER MODULE           ║{Colors.RESET}")
    print(f"{Colors.CYAN}{Colors.BOLD}║                    ENUMARATE THE TARGET                ║{Colors.RESET}")
    print(f"{Colors.CYAN}{Colors.BOLD}╚════════════════════════════════════════════════════════╝{Colors.RESET}\n")
    userinput = input(f"{Colors.GREEN}[?]{Colors.RESET} Enter target domain or IP: ").strip()
    if not userinput:
        print(f"{Colors.RED}[!]{Colors.RESET} Target cannot be empty!")
        return
    scanner = PortScanner(userinput)
    loading_animation("[*] Resolving target")
    ip = scanner.resolve_target()
    if not ip:
        return 
    loading_animation("[*] Initializing full port scan")
    elapsed = scanner.scan_all_ports(ip, threads=300)
    scanner.print_results(elapsed)
    input(f"\n{Colors.YELLOW}Press Enter to continue...{Colors.RESET}")


def enumeration():
    port_scan()


if __name__ == "__main__":
    enumeration()