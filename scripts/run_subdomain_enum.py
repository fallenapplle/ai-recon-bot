import sys
import os
import argparse



sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from modules.subdomain_recon import main

class Colors:
    # Reset
    ENDC = '\033[0m'

    # Regular Colors
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'

    # Bold
    BRED = '\033[1;31m'
    BGREEN = '\033[1;32m'
    BYELLOW = '\033[1;33m'
    BBLUE = '\033[1;34m'
    BMAGENTA = '\033[1;35m'
    BCYAN = '\033[1;36m'

    # Underline
    URED = '\033[4;31m'
    UWHITE = '\033[4;37m'

def color_print(text, color=Colors.ENDC, end="\n"):
    print(f"{color}{text}{Colors.ENDC}", end=end)

def validate_file(path):
    if not os.path.isfile(path):
        raise argparse.ArgumentTypeError(f"{Colors.RED}File '{path}' does not exist{Colors.ENDC}")
    if os.path.getsize(path) == 0:
        raise argparse.ArgumentTypeError(f"{Colors.RED}File '{path}' is empty{Colors.ENDC}")
    return path

def read_domains_from_file(file_path):
    with open(file_path, 'r') as f:
        return [line.strip() for line in f.readlines() if line.strip()]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=f'{Colors.BLUE}Subdomain Enumeration Tool{Colors.ENDC}',
        formatter_class=argparse.RawTextHelpFormatter,
        epilog=f'''{Colors.CYAN}
Examples:
  {Colors.WHITE}Interactive mode: {Colors.GREEN}python script.py
  {Colors.WHITE}Single domain:    {Colors.GREEN}python script.py -d example.com
  {Colors.WHITE}File input:       {Colors.GREEN}python script.py -f domains.txt{Colors.ENDC}'''
    )

    input_group = parser.add_mutually_exclusive_group()
    input_group.add_argument('-d', '--domain', 
                           help='Single domain to analyze')
    input_group.add_argument('-f', '--file', 
                           type=validate_file,
                           help='Text file containing list of domains')

    args = parser.parse_args()

    domains = []
    
    try:
        if args.file:
            domains = read_domains_from_file(args.file)
            color_print(f"\n[+] Loaded {len(domains)} domains from file", Colors.BGREEN)
        elif args.domain:
            domains = [args.domain]
        else:
            color_print("\nEnter domain or file path (press Ctrl+C to exit): ", Colors.BYELLOW, end="")
            user_input = input().strip()
            
            if os.path.isfile(user_input):
                domains = read_domains_from_file(user_input)
                color_print(f"\n[+] Loaded {len(domains)} domains from file", Colors.BGREEN)
            else:
                domains = [user_input]

        for idx, domain in enumerate(domains, 1):
            color_print(f"\n=== Processing domain {idx}/{len(domains)}: {domain} ===", Colors.BCYAN)
            try:
                main(domain)
            except Exception as e:
                color_print(f"[!] Error processing {domain}: {str(e)}", Colors.BRED)
                continue

        color_print("\n[+] All domains processed successfully!", Colors.BGREEN)

    except KeyboardInterrupt:
        color_print("\n[!] Operation cancelled by user", Colors.BRED)
        sys.exit(0)