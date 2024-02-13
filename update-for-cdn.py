import csv
import requests

LINODE_API_URL = "https://api.linode.com/v4/domains"
LINODE_TOKEN = "your_linode_api_token_here"

def fetch_linode_domains():
    headers = {"Authorization": f"Bearer {LINODE_TOKEN}"}
    domains_dict = {}
    page = 1

    while True:
        response = requests.get(f"{LINODE_API_URL}?page={page}", headers=headers)
        if response.ok:
            data = response.json()['data']
            for domain in data:
                domain_name = domain['domain'].strip().lower()
                domain_id = domain['id']
                domains_dict[domain_name] = domain_id
            
            if page >= response.json()['pages']:
                break
            page += 1
        else:
            print(f"Failed to fetch domains from Linode. Status Code: {response.status_code}")
            break

    return domains_dict

def add_www_cname_record(domain_id, cname_target="champion1.edgesuite.net"):
    headers = {
        "Authorization": f"Bearer {LINODE_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "type": "CNAME",
        "name": "www",
        "target": cname_target,
        "ttl_sec": 300
    }
    response = requests.post(f"{LINODE_API_URL}/{domain_id}/records", headers=headers, json=data)
    if response.status_code in [200, 201]:
        print(f"Added 'www' CNAME record for domain ID: {domain_id} pointing to {cname_target}")
    else:
        print(f"Failed to add 'www' CNAME record for domain ID: {domain_id}. Status Code: {response.status_code}, Response: {response.text}")

def read_domains_from_csv(csv_file_path):
    with open(csv_file_path, mode='r') as file:
        csv_reader = csv.reader(file)
        domains = set()
        for row in csv_reader:
            domain = row[0].strip().lower()
            if domain.startswith('www.'):
                domain = domain[4:]  # Correctly removes the 'www.' prefix
            domains.add(domain)
        return domains

def main(csv_file_path):
    domain_names = read_domains_from_csv(csv_file_path)
    linode_domains = fetch_linode_domains()

    for domain in domain_names:
        if domain in linode_domains:
            domain_id = linode_domains[domain]
            add_www_cname_record(domain_id)
        else:
            print(f"Domain {domain} not found in Linode DNS Manager.")

# Ensure to fill in the actual path to your CSV file
csv_file_path = "path_to_your_csv_file.csv"
main(csv_file_path)
