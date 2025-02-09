import os 
from dotenv import load_dotenv


load_dotenv()

Shodan_api_key = os.getenv("SHODAN_API_KEY")


print(f"Shodan APi key is: {Shodan_api_key}  ")
