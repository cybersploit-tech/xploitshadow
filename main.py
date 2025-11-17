#!/usr/bin/env python3
import os
import sys
import time
from utils.animation import loading_animation
from utils.ColorsX import Colors
from utils.bg import print_banner, print_menu
from enumaration.enumarate import port_scan 

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def enumeration_mode():
    clear_screen()
    port_scan()
    
def find_vulnerabilities():
    clear_screen()

def exploitation_mode():
    clear_screen()
def main():
    while True:
        clear_screen()
        print_banner()
        print_menu()
        try:
            choice = input(f"\n{Colors.CYAN}[XPloit]{Colors.RESET} Select option: ").strip()
            if choice == '1':
                enumeration_mode()
            elif choice == '2':
                find_vulnerabilities()
            elif choice == '3':
                exploitation_mode()
            elif choice == '0':
                print(f"\n{Colors.GREEN}[+]{Colors.RESET} Exiting XPloit Tool...")
                time.sleep(1)
                clear_screen()
                sys.exit(0)
            else:
                print(f"\n{Colors.RED}[!]{Colors.RESET} Invalid option!")
                time.sleep(1)
        except KeyboardInterrupt:
            print(f"\n\n{Colors.RED}[!]{Colors.RESET} Interrupted by user")
            time.sleep(1)
            clear_screen()
            sys.exit(0)
        except Exception as e:
            print(f"\n{Colors.RED}[!]{Colors.RESET} Error: {e}")
            
if __name__ == "__main__":
    main()