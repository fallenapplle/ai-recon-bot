import subprocess
import os
import shutil
from modules.alive_checker import check_alive , save_alive_to_file 

class Colors:
    ENDC = '\033[0m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    CYAN = '\033[36m'
    BRED = '\033[1;31m'
    BGREEN = '\033[1;32m'
    BYELLOW = '\033[1;33m'
    BBLUE = '\033[1;34m'

def color_print(text, color=Colors.ENDC, end="\n"):
    print(f"{color}{text}{Colors.ENDC}", end=end)

def check_tools():
    required_tools = ['subfinder', 'assetfinder']
    for tool in required_tools:
        if not shutil.which(tool):
            color_print(f"[!] Required tool '{tool}' not found in PATH", Colors.BRED)
            raise SystemExit()

def validate_domain(domain):
    domain = domain.strip().lower()
    for prefix in ('http://', 'https://', 'www.'):
        domain = domain.replace(prefix, '')
    if '.' not in domain or ' ' in domain:
        color_print(f"[!] Invalid domain format: {domain}", Colors.BRED)
        raise ValueError()
    return domain

def run_subfinder(domain):
    color_print("[*] Running Subfinder...", Colors.BYELLOW)
    try:
        result = subprocess.run(
            ["subfinder", "-d", domain],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            check=True
        )
        color_print("[+] Subfinder scan completed!", Colors.BGREEN)
        return result.stdout.decode().splitlines()
    except Exception as e:
        color_print(f"[!] Subfinder error: {str(e)}", Colors.BRED)
        return []

def run_assetsfinder(domain):
    color_print("[*] Running Assetfinder...", Colors.BYELLOW)
    try:
        result = subprocess.run(
            ["assetfinder", "--subs-only", domain],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            check=True
        )
        color_print("[+] Assetfinder scan completed!", Colors.BGREEN)
        return result.stdout.decode().splitlines()
    except Exception as e:
        color_print(f"[!] Assetfinder error: {str(e)}", Colors.BRED)
        return []

def save_subdomains_to_file(subdomains, domain, filepath="data"):
    os.makedirs(filepath, exist_ok=True)
    filename = f"{domain}-subdomains.txt"
    full_path = os.path.join(filepath, filename)
    
    cleaned_subs = sorted({sub.strip() for sub in subdomains if sub.strip()})
    
    if not cleaned_subs:
        color_print("[!] No subdomains found to save", Colors.BRED)
        return

    try:
        with open(full_path, "w") as f:
            f.write("\n".join(cleaned_subs))
        color_print(f"[+] Saved {len(cleaned_subs)} subdomains to: {full_path}", Colors.BBLUE)
    except IOError as e:
        color_print(f"[!] File save error: {str(e)}", Colors.BRED)

def main(domain):
    check_tools()
    try:
        clean_domain = validate_domain(domain)
    except ValueError:
        return

    color_print(f"\n[+] Starting subdomain enumeration for: {clean_domain}", Colors.BGREEN)
    
    subdomains = set()
    subdomains.update(run_subfinder(clean_domain))
    subdomains.update(run_assetsfinder(clean_domain))
    
    color_print(f"\n[+] Total unique subdomains found: {len(subdomains)}", Colors.BBLUE)
    
    if subdomains:
        save_subdomains_to_file(subdomains, clean_domain)


        alive = check_alive(subdomains)
        if alive:
            save_alive_to_file(alive, clean_domain)
    else:
        color_print("[!] No subdomains discovered", Colors.BRED)
    


if __name__ == "__main__":
    try:
        domain = input("\nEnter target domain: ")
        main(domain)
    except KeyboardInterrupt:
        color_print("\n[!] Operation cancelled", Colors.BRED)