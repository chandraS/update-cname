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
        if response.ok:  # Checks for successful status codes (200-299)
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

def fetch_domain_records(domain_id):
    headers = {"Authorization": f"Bearer {LINODE_TOKEN}"}
    response = requests.get(f"{LINODE_API_URL}/{domain_id}/records", headers=headers)
    if response.ok:
        return response.json()['data']
    else:
        print(f"Failed to fetch DNS records for domain ID: {domain_id}. Status Code: {response.status_code}")
        return []

def delete_dns_record(domain_id, record_id):
    headers = {"Authorization": f"Bearer {LINODE_TOKEN}"}
    response = requests.delete(f"{LINODE_API_URL}/{domain_id}/records/{record_id}", headers=headers)
    if response.status_code in [200, 204]:  # 204 No Content for successful deletion without response body
        print(f"Deleted DNS record ID: {record_id} for domain ID: {domain_id}")
    else:
        print(f"Failed to delete DNS record ID: {record_id} for domain ID: {domain_id}. Status Code: {response.status_code}, Response: {response.text}")

def read_domains_from_csv(csv_file_path):
    with open(csv_file_path, mode='r') as file:
        csv_reader = csv.reader(file)
        return [(row[0].strip().lower(), row[1].strip(), row[2].strip()) for row in csv_reader]

def main(csv_file_path):
    domain_details = read_domains_from_csv(csv_file_path)
    linode_domains = fetch_linode_domains()

    for domain, cname, target in domain_details:
        if domain in linode_domains:
            domain_id = linode_domains[domain]
            dns_records = fetch_domain_records(domain_id)
            for record in dns_records:
                if record['type'] == 'CNAME' and record['name'].strip().lower() == cname.strip().lower() and record['target'].strip() == target.strip():
                    delete_dns_record(domain_id, record['id'])

csv_file_path = "path_to_your_csv_file.csv"
main(csv_file_path)
