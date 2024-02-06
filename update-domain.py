import requests

# Linode API token
api_token = 'YOUR_API_TOKEN'

# Path to the text file containing domain details
file_path = 'domains.txt'

# Linode API endpoint URL for listing domains
list_domains_url = 'https://api.linode.com/v4/domains'

# Headers with API token
headers = {
    'Authorization': f'Bearer {api_token}',
    'Content-Type': 'application/json',
}

def update_cname(domain_name, subdomain, target, ttl_sec):
    # Send a GET request to list domains
    response = requests.get(list_domains_url, headers=headers)

    if response.status_code == 200:
        domains = response.json()
        for domain in domains:
            if domain['domain'] == domain_name:
                domain_id = domain['id']
                break
        else:
            print(f"Domain '{domain_name}' not found.")
            return

        # New CNAME record data
        new_cname = {
            "type": "CNAME",
            "name": subdomain,
            "target": target,
            "ttl_sec": ttl_sec
        }

        # Update the CNAME record using the retrieved domain ID
        update_record_url = f'https://api.linode.com/v4/domains/{domain_id}/records'
        response = requests.post(update_record_url, headers=headers, json=new_cname)

        if response.status_code == 200:
            print(f'CNAME record updated successfully for domain: {domain_name}')
        else:
            print(f'Failed to update CNAME record for domain: {domain_name}. Status code: {response.status_code}')
            print(response.text)
    else:
        print('Failed to list domains. Status code:', response.status_code)
        print(response.text)

# Read domain details from the text file and update CNAME records
with open(file_path, 'r') as file:
    for line in file:
        domain_name, subdomain, target, ttl_sec = line.strip().split(',')
        update_cname(domain_name, subdomain, target, int(ttl_sec))
