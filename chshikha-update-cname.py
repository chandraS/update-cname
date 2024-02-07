import csv
import requests

# Linode API URL for DNS domains
LINODE_API_URL = "https://api.linode.com/v4/domains"
# Your Linode Personal Access Token
LINODE_TOKEN = "your_linode_api_token_here"

# Function to fetch domains from Linode API
def fetch_linode_domains():
    headers = {"Authorization": f"Bearer {LINODE_TOKEN}"}
    response = requests.get(LINODE_API_URL, headers=headers)
    if response.status_code == 200:
        return {domain['domain']: domain['id'] for domain in response.json()['data']}
    else:
        print("Failed to fetch domains from Linode")
        return {}

# Modified function to read domain names, CNAME, and targets from a CSV file
def read_domains_from_csv(csv_file_path):
    with open(csv_file_path, mode='r') as file:
        csv_reader = csv.reader(file)
        # Assuming the CSV has columns: domain, cname, target
        return [(row[0], row[1], row[2]) for row in csv_reader]

# Function to update or add CNAME record for a given domain
def update_cname_record(domain_id, cname, target):
    headers = {"Authorization": f"Bearer {LINODE_TOKEN}", "Content-Type": "application/json"}
    # Check if CNAME exists and update or create accordingly (simplified here for brevity)
    data = {
        "type": "CNAME",
        "name": cname,
        "target": target,
        "ttl_sec": 300
    }
    response = requests.post(f"{LINODE_API_URL}/{domain_id}/records", headers=headers, json=data)
    if response.status_code in [200, 201]:  # 201 for created, 200 for other successful responses
        print(f"Updated/Added CNAME record for domain ID: {domain_id}")
    else:
        print(f"Failed to update/add CNAME record for domain ID: {domain_id}, Status Code: {response.status_code}")

# Main function to tie everything together
def main(csv_file_path):
    domain_details = read_domains_from_csv(csv_file_path)
    linode_domains = fetch_linode_domains()

    for domain, cname, target in domain_details:
        if domain in linode_domains:
            update_cname_record(linode_domains[domain], cname, target)
        else:
            print(f"Domain {domain} not found in Linode DNS Manager.")

# Example usage
csv_file_path = "path_to_your_csv_file.csv"
main(csv_file_path)
