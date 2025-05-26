import requests
import csv
from datetime import datetime
import json
import base64
import logging
import os
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)

# Jira URL and authentication details
jira_url = "https://[your_company].atlassian.net/rest/api/2/search"
token = "[your_token]"

# Jira API details (from environment variables)
jira_url = os.getenv("JIRA_URL", jira_url)
token = os.getenv("JIRA_API_TOKEN", token)
email = os.getenv("JIRA_EMAIL", "[your_email]")
auth = base64.b64encode(f"{email}:{token}".encode("utf-8")).decode("utf-8")
headers = {
    "Authorization": f"Basic {auth}",
    "Content-Type": "application/json"
}

# Initialize counters and data storage
all_issues = []
issues_data = []  # List to store all issue data for CSV export
start_at = 0
fixed_by_liveops_count = 0
change_caused_by_count = 0
max_results = 100

# CSV filename with timestamp
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
csv_filename = f"jira_issues_export_{timestamp}.csv"

# Define CSV headers
csv_headers = [
    'Key', 'Priority', 'Incident Start', 'Fault Caused By', 'Area', 
    'Function', 'Duration', 'Response Time', 'Turn Over Drop', 'Change Caused By', 'Change Caused By Key'
]

while True:
    jql_query = {
        "jql": 'project = INC AND priority in (P1, P2, P3, P4) AND "Incident Start" >= startOfWeek (-2) AND "Incident Start" < endOfWeek(-1) ORDER BY key desc',
        
        "maxResults": max_results,
        "startAt": start_at,
        "fields": [
            "key", 
            "priority", 
            "created",
            "customfield_12309",  # INC Start
            "customfield_12310",  # INC End date
            "customfield_12503",  # INC Duration
            "customfield_13839",  # Trigger
            "customfield_14021",  # Fault caused by
            "customfield_13847",  # Turnover drop
            "customfield_13146",  # Response time
            "customfield_14005",  # Responder
            "customfield_13079",  # Root Cause Found
            "customfield_13075",  # Fix Date
            "customfield_14022",  # Function
            "customfield_14015",  # Brands
            "issuelinks", "resolution",
            "customfield_13991",  # Area
            "customfield_13840",  # Monitoring trigger
            "customfield_13857",  # Reported time
            "issuetype"
        ],
        "expand": "names,customfield_14021.cmdb.label,customfield_14005.cmdb.label,customfield_14005.cmdb.objectKey,customfield_14005.cmdb.attributes,customfield_13991.cmdb.label,customfield_14015.cmdb.label,customfield_14022.cmdb.label"
    }

    # Send the GET request
    response = requests.get(jira_url, headers=headers, params=jql_query)

    if response.status_code == 200:
        data = response.json()
        logging.info(f"Found {data['total']} resolved incidents in project 'INC'")
        total_incidents = 0
        issues = data.get('issues', [])
        all_issues.extend(issues)
        
        for issue in data.get('issues', []):
            fields = issue.get('fields', {})

            # Extract required fields
            incident_start = fields.get('customfield_12309', 'N/A')
            incident_end = fields.get('customfield_12310', 'N/A') 
            reported_time = fields.get('customfield_13857', 'N/A')
            response_time = fields.get('customfield_13146', 'N/A')
            turn_over_drop = fields.get('customfield_13847', 'N/A')
            duration = fields.get('customfield_12503', 'N/A')
            
            responder_data = fields.get('customfield_14005', [])
            responder = ', '.join(obj.get('label', 'Unknown') for obj in responder_data) or 'N/A'
            area_data = fields.get('customfield_13991', [])
            area = ', '.join(obj.get('label', 'Unknown') for obj in area_data) or 'N/A'
            brands_data = fields.get('customfield_14015', [])
            brands = ', '.join(obj.get('label', 'Unknown') for obj in brands_data) or 'N/A'
            function_data = fields.get('customfield_14022', [])
            function = ', '.join(obj.get('label', 'Unknown') for obj in function_data) or 'N/A'

            fix_date_field = fields.get("customfield_13075")
            fix_date = fix_date_field.get("value", "N/A") if fix_date_field else "N/A"
            
            resolution_data = fields.get("resolution")
            if isinstance(resolution_data, dict):
                resolution = resolution_data.get("name", "N/A")
            else:
                resolution = "N/A"
            
            trigger = fields.get("customfield_13839")
            trigger = trigger.get("value", "N/A") if trigger else "N/A"

            root_cause_found = fields.get("customfield_13079")
            root_cause_found = root_cause_found.get("value", "N/A") if root_cause_found else "N/A"

            monitoring_trigger_field = fields.get("customfield_13840")
            monitoring_trigger = monitoring_trigger_field.get("value", "N/A") if monitoring_trigger_field else "N/A"
        
            # Format duration if present
            formatted_duration = f"{int(duration)}" if duration else "N/A"
            
            # Retrieve linked issues and their relationships
            issuelinks = fields.get('issuelinks', [])
            linked_issues_info = [
                (link[issue_key]['key'], link['type'].get(relation_key, 'N/A'))
                for link in issuelinks
                for issue_key, relation_key in [('inwardIssue', 'inward'), ('outwardIssue', 'outward')]
                if issue_key in link
            ]

            # Extract issue keys based on relationship types
            caused_by_keys = [issue for issue, relation in linked_issues_info if relation == "is caused by"]
            relates_to_keys = [issue for issue, relation in linked_issues_info if relation == "relates to"]
            resolved_by_keys = [issue for issue, relation in linked_issues_info if relation == "is resolved by"]

            is_caused_by = bool(caused_by_keys)
            is_related_to = bool(relates_to_keys)
            is_resolved_by = bool(resolved_by_keys)

            caused_by_fields = ', '.join(caused_by_keys) if caused_by_keys else "N/A"
            related_to_fields = ', '.join(relates_to_keys) if relates_to_keys else "N/A"
            resolved_by_fields = ', '.join(resolved_by_keys) if resolved_by_keys else "N/A"

            # Fixed by LiveOps check
            fixed_by_liveops = "No"
            # Extracting Fault Caused By values
            fault_caused_by_data = fields.get('customfield_14021', [])
            fault_caused_by_list = [obj.get('label', 'Unknown') for obj in fault_caused_by_data]
            fault_caused_by = ', '.join(fault_caused_by_list) or 'N/A'
            change_caused_by = False
            change_caused_by_key = "N/A"

            # List of excluded "Fault Caused By" values
            excluded_fault_causes = {"Provider", "Government", "Internet_Service"}

            issue_type = fields.get('issuetype', {}).get('name', '')

            # Check if issue is "Operations" and resolution is valid
            if issue_type == "Operations" and resolution != "Not an issue":
                for linked_key, linked_type in [
                    (link[issue_key]['key'], link[issue_key].get('fields', {}).get('issuetype', {}).get('name', ''))
                    for link in issuelinks
                    for issue_key in ['inwardIssue', 'outwardIssue']
                    if issue_key in link
                ]:
                    if linked_key.startswith("PRB") and linked_type == "Known Issue":
                        fixed_by_liveops = "Yes"
                        fixed_by_liveops_count += 1
                        break
                        
                for linked_key, relation in linked_issues_info:
                    if relation == "is caused by" and not any(cause in excluded_fault_causes for cause in fault_caused_by_list):
                        change_caused_by = True
                        change_caused_by_key = linked_key
                        change_caused_by_count += 1
                        break
                        
            total_incidents += 1
            
            # Get all linked issue keys
            linked_issue_keys = [
                link[issue_key]['key']
                for link in issuelinks
                for issue_key in ['inwardIssue', 'outwardIssue']
                if issue_key in link
            ]

            # Prepare data row for CSV
            issue_row = [
                issue.get('key', 'N/A'),
                fields.get('summary', 'N/A'),
                issue_type,
                fields.get('description', 'N/A'),
                fields.get('status', {}).get('name', 'N/A'),
                fields.get('priority', {}).get('name', 'N/A'),
                fields.get('created', 'N/A'),
                incident_start,
                incident_end,
                fault_caused_by,
                responder,
                area,
                brands,
                function,
                formatted_duration,
                trigger,
                fix_date,
                monitoring_trigger,
                reported_time,
                root_cause_found,
                response_time,
                resolution,
                ', '.join(linked_issue_keys) if linked_issue_keys else 'N/A',
                turn_over_drop,
                is_caused_by,
                caused_by_fields,
                is_related_to,
                related_to_fields,
                is_resolved_by,
                resolved_by_fields,
                fixed_by_liveops,
                change_caused_by,
                change_caused_by_key
            ]
            
            issues_data.append(issue_row)

        logging.info(f"Total issues fetched: {len(all_issues)}")
        logging.info(f"Fixed by LiveOps count: {fixed_by_liveops_count}")
        logging.info(f"Change caused by count: {change_caused_by_count}")
        logging.info(f"Total Incidents: {total_incidents}")
        
        if len(issues) < max_results:
            logging.info("Fetched the last batch of issues.")
            break
            
        start_at += max_results
    else:
        logging.error(f"Failed to fetch data: {response.status_code} - {response.text}")
        break

# Write data to CSV file
try:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(script_dir, csv_filename)
    
    with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        
        # Write headers
        writer.writerow(csv_headers)
        
        # Write data rows
        writer.writerows(issues_data)
    
    logging.info(f"Successfully exported {len(issues_data)} issues to: {csv_path}")
    logging.info(f"CSV file saved as: {csv_filename}")
    
except Exception as e:
    logging.error(f"Error writing to CSV file: {str(e)}")

# Print summary statistics
print(f"\n{'='*50}")
print(f"EXPORT SUMMARY")
print(f"{'='*50}")
print(f"Total issues exported: {len(issues_data)}")
 print(f"Fixed by LiveOps count: {fixed_by_liveops_count}")
print(f"Change caused by count: {change_caused_by_count}")
print(f"CSV file location: {csv_path}")
print(f"{'='*50}")
