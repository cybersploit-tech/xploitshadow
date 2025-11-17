import sys
import time
from utils.ColorsX import  Colors
def loading_animation(text, duration=2):
    chars = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"
    end_time = time.time() + duration
    i = 0
    while time.time() < end_time:
        sys.stdout.write(f'\r{Colors.CYAN}{text} {chars[i % len(chars)]}{Colors.RESET}')
        sys.stdout.flush()
        time.sleep(0.1)
        i += 1
    sys.stdout.write(f'\r{Colors.GREEN}{text} ✓{Colors.RESET}\n')