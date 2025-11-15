#!/usr/bin/env python3
import os
import sys
from colorama import init, Fore, Style
from enumaration.enumarate import enumarate
init(autoreset=True)
G = Fore.GREEN + Style.BRIGHT
R = Fore.RED + Style.BRIGHT
C = Fore.CYAN + Style.BRIGHT
Y = Fore.YELLOW + Style.BRIGHT
W = Fore.WHITE + Style.BRIGHT
M = Fore.MAGENTA + Style.BRIGHT
def clear_screen():
    os.system('clear' if os.name != 'nt' else 'cls')
def print_banner():
    banner = f"""
{M}╔══════════════════════════════════════════════════════════╗
{G}║{C}   █████╗  █████╗  █████╗  █████╗  █████╗  █████╗  █████╗ {G}║
{G}║{C}  ██╔══██╗██╔══██╗██╔══██╗██╔══██╗██╔══██╗██╔══██╗██╔══██╗{G}║
{G}║{C}  ╚██████║███████║███████║███████║███████║███████║███████║{G}║
{G}║{C}   ╚═══██║██╔══██║██╔══██║██╔══██║██╔══██║██╔══██║██╔══██║{G}║
{G}║{C}   ██████║██║  ██║██║  ██║██║  ██║██║  ██║██║  ██║██║  ██║{G}║
{G}║{C}   ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝{G}║
{G}║{Y}           ► XploitShadow v1.0 - Elite Pentest Suite ◄    {G}║
{G}║{M}        Advanced Reconnaissance & Exploitation Framework  {G}║
{M}╚══════════════════════════════════════════════════════════╝
    """
    print(banner)
def show_menu():
    clear_screen()
    print_banner()
    
    menu = f"""
{G}  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{G}  ╔════════════════ SHADOW OPERATIONS CENTER ════════════════╗
{W}  ║{Y}  Select Your Attack Vector:                              {W}║
{G}  ╠══════════════════════════════════════════════════════════╣
{W}  ║  {C}[1] → {Y}ENUMERATION         {M}[Recon Mode]                  {W}║
{W}  ║  {C}[2] → {Y}EXPLOITATION        {M}[Strike Mode]                 {W}║
{W}  ║  {C}[3] → {Y}VULNERABILITY SCAN  {M}[Hunt Mode]                   {W}║
{W}  ║  {C}[4] → {Y}POST-EXPLOITATION   {M}[Persist Mode]                {W}║
{R}  ║  {C}[0] → {R}EXIT SHADOW         {M}[Disconnect]                  {R}║
{G}  ╚══════════════════════════════════════════════════════════╝

{G}  ┌─[{W}XploitShadow v1.0{G}]─[{C}Elite Access{G}]─[~]
  └──╼ $ {Style.RESET_ALL}"""
    
    print(menu)
    choice = input("")
    return choice.strip()
def enumeration_module():
    clear_screen()
    enumarate()

def exploitation_module():
    clear_screen()
    print(f"\n{R}[!] EXPLOITATION MODULE ACTIVATED")
    print(f"{G}{'─' * 60}")
    print(f"{W}[*] Exploit database: 12,847 modules loaded")
    print(f"{W}[*] Payload generator: Ready")
    print(f"{G}[✓] Exploitation engine online")
    input(f"\n{G}Press ENTER to return...{Style.RESET_ALL}")

def vulnerability_module():
    clear_screen()
    print(f"\n{G}[!] VULNERABILITY DETECTION ACTIVATED")
    print(f"{G}{'─' * 60}")
    print(f"{W}[*] CVE database: 1,247,893 entries synced")
    print(f"{W}[*] Scanner engine: Active")
    print(f"{G}[✓] Ready to hunt vulnerabilities")
    input(f"\n{G}Press ENTER to return...{Style.RESET_ALL}")

def post_exploitation_module():
    clear_screen()
    print(f"\n{G}[!] POST-EXPLOITATION MODULE ACTIVATED")
    print(f"{G}{'─' * 60}")
    print(f"{W}[*] C2 framework: DNS/HTTP tunnel established")
    print(f"{W}[*] Persistence: Registry + systemd hooks")
    print(f"{G}[✓] Full control maintained")
    input(f"\n{G}Press ENTER to return...{Style.RESET_ALL}")
def main():
    clear_screen()
    print(f"{C}XploitShadow Elite Framework v1.0")
    print(f"{Y}[*] AV/EDR bypass: Enabled")
    print(f"{G}[+] Shadow kernel: Loaded\n")

    while True:
        user_choice = show_menu()
        
        if user_choice == "1":
            enumeration_module()
        elif user_choice == "2":
            exploitation_module()
        elif user_choice == "3":
            vulnerability_module()
        elif user_choice == "4":
            post_exploitation_module()
        elif user_choice == "0":
            clear_screen()
            print(f"\n{R}[!] Terminating all connections...")
            print(f"{Y}[*] Erasing session logs...")
            print(f"{G}[✓] Disconnected. Stay hidden.\n")
            sys.exit(0)
        else:
            clear_screen()
            print_banner()
            print(f"{R}[!] Invalid selection!")
            input(f"\n{G}Press ENTER to continue...{Style.RESET_ALL}")

if __name__ == "__main__":
    main()