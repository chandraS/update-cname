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
        if response.status_code == 200:
            data = response.json()['data']
            for domain in data:
                domain_name = domain['domain'].strip().lower()  # Normalize domain name
                domain_id = domain['id']
                domains_dict[domain_name] = domain_id
            
            # Check if there are more pages
            if page >= response.json()['pages']:
                break
            page += 1
        else:
            print("Failed to fetch domains from Linode")
            break

    return domains_dict

def read_domains_from_csv(csv_file_path):
    with open(csv_file_path, mode='r') as file:
        csv_reader = csv.reader(file)
        # Normalize domain name, remove potential whitespace, and make case-insensitive
        return [(row[0].strip().lower(), row[1].strip(), row[2].strip()) for row in csv_reader]

def update_cname_record(domain_id, cname, target):
    headers = {
        "Authorization": f"Bearer {LINODE_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "type": "CNAME",
        "name": cname,
        "target": target,
        "ttl_sec": 300
    }
    response = requests.post(f"{LINODE_API_URL}/{domain_id}/records", headers=headers, json=data)
    if response.status_code in [200, 201]:
        print(f"Updated/Added CNAME record for domain ID: {domain_id}")
    else:
        print(f"Failed to update/add CNAME record for domain ID: {domain_id}, Status Code: {response.status_code}")

def main(csv_file_path):
    domain_details = read_domains_from_csv(csv_file_path)
    linode_domains = fetch_linode_domains()

    for domain, cname, target in domain_details:
        if domain in linode_domains:
            update_cname_record(linode_domains[domain], cname, target)
        else:
            print(f"Domain {domain} not found in Linode DNS Manager.")

csv_file_path = "path_to_your_csv_file.csv"
main(csv_file_path)
