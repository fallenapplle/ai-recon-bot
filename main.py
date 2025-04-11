import os 
from modules import subdomain_recon

Shodan_api_key = os.getenv("SHODAN_API_KEY")


print(f"Shodan APi key is: {Shodan_api_key}  ")



if __name__ == "__main__":

    domain = input("Enter your Target Name: ")
    subdomain_recon.enumerate_subdomains(domain)
