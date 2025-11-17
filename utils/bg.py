from utils.ColorsX import Colors
def print_banner():
    banner = f"""
{Colors.CYAN}{Colors.BOLD}
    ╔═════════════════════════════════════════════════════════╗
    ║                                                         ║
    ║         ██╗  ██╗██████╗ ██╗      ██████╗ ██╗████████╗   ║
    ║         ╚██╗██╔╝██╔══██╗██║     ██╔═══██╗██║╚══██╔══╝   ║
    ║          ╚███╔╝ ██████╔╝██║     ██║   ██║██║   ██║      ║
    ║          ██╔██╗ ██╔═══╝ ██║     ██║   ██║██║   ██║      ║
    ║         ██╔╝ ██╗██║     ███████╗╚██████╔╝██║   ██║      ║
    ║         ╚═╝  ╚═╝╚═╝     ╚══════╝ ╚═════╝ ╚═╝   ╚═╝      ║
    ║                                                         ║
    ║            Advanced Exploitation Tool                   ║
    ║                  Version 1.0                            ║
    ╚═════════════════════════════════════════════════════════╝
{Colors.RESET}
    """
    print(banner)

def print_menu():
    menu = f"""
{Colors.GREEN}    ┌─────────────────────────────────────┐
    │        SELECT OPERATION MODE        │
    ├─────────────────────────────────────┤{Colors.RESET}
    │                                     │
    │  {Colors.CYAN}[1]{Colors.RESET} Enumeration                    │
    │  {Colors.CYAN}[2]{Colors.RESET} Find Vulnerabilities           │
    │  {Colors.CYAN}[3]{Colors.RESET} Exploitation                   │
    │                                     │
    │  {Colors.RED}[0]{Colors.RESET} Exit                           │
    │                                     │
{Colors.GREEN}    └─────────────────────────────────────┘{Colors.RESET}
    """
    print(menu)