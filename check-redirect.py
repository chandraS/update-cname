import requests

def check_redirection(domain):
    try:
        # Make a GET request to the domain and allow redirection
        response = requests.get(f"http://{domain}", allow_redirects=True)
        final_url = response.url  # Get the final URL after following redirects
        
        # Check if the final URL does not start with 'www'
        if not final_url.startswith('http://www.'):
            print(f"{domain} redirects to a non-www address: {final_url}")
        else:
            print(f"{domain} does not redirect to a non-www address")
    except requests.RequestException as e:
        print(f"Failed to check redirection for {domain}: {e}")

# Path to the text file containing domain names
file_path = 'domains.txt'

# Read domain names from the text file
with open(file_path, 'r') as file:
    domains_to_check = [line.strip() for line in file]

# Check redirection for each domain
for domain in domains_to_check:
    check_redirection(domain)
