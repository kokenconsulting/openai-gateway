#!/usr/bin/env python3.10
import argparse
import os
from datetime import datetime
import requests
import pprint as pprint
import json

# get base url from env variables
base_url = os.environ.get('BASE_URL', 'http://localhost:5001')
teams_webhook_url = os.environ.get('TEAMS_WEBHOOK_URL')

def main():
    parser = argparse.ArgumentParser(description="OPEN AI GATEWAY CLI TOOL")
    parser.add_argument("query", type=str, help="Query")
    parser.add_argument('--save', action=argparse.BooleanOptionalAction)
    parser.add_argument('--load', action=argparse.BooleanOptionalAction)

    args = parser.parse_args()
    if args.load:
        print("Loading...")
        build_index()
    
    if args.query:
        print(f"Q: {args.query}")
        ail_query(args.query)
        
def build_index():
    # call localhost:5001 to build index using requests library
    response = requests.get(base_url +'/index')
    if response.status_code == 200:
        print('Index built successfully!')
    else:
        print('Error building index:', response.text)

def ail_query(query_input):
    url = base_url +'/query'
    data = {
        "query": query_input,
        "skip_price_calc": False,
    }
    if teams_webhook_url:
        data['teams_webhook_url'] = teams_webhook_url

    response = requests.post(url, json=data)
    if response.status_code == 200:
        json_response = response.json()
        print(json_response['query_response'])
        pprint.pprint(json.dumps(json_response, indent=2))
    else:
        print('Error:', response.text)

if __name__ == "__main__":
    main()