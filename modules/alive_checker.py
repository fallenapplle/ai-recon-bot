import requests 

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

def check_alive(subdomains):
    alive = []

    print(f"\n[+] Checking alive subdomains....\n")

    for subdomain in subdomains:
        url = f"http://{subdomain}"
        try:
            response = requests.get(url, timeout=3)
            if response.status_code < 500:
                alive.append(subdomain)
                print(f"[+] Subdomain {Colors.BGREEN}{subdomain}{Colors.ENDC} is alive.")

        except requests.RequestException:
            pass
    return alive

def save_alive_to_file(alive_subdomain, filename_prefix):
    filename = f"data/{filename_prefix}-alive.txt"
    with open (filename, 'w') as f:
        for subdomain in alive_subdomain:
            f.write(f"{subdomain}\n")
    print(f"[+] Saved {len(alive_subdomain)} alive subdomain to {filename}")


