from jira import JIRA 
import pandas as pd
from datetime import datetime
import os
from dotenv import load_dotenv


load_dotenv()


jira_url = os.getenv("JIRA_URL")
jira_user = os.getenv("JIRA_USER")
jira_api_token = os.getenv("JIRA_API_TOKEN")
assignee_id = os.getenv("JIRA_ASSIGNEE_ID")  


jira = JIRA(server=jira_url, basic_auth=(jira_user, jira_api_token))


def get_working_days(year=2025):
    start_date = datetime(year, 4, 1)
    end_date = datetime(year, 5, 22)  
    return pd.bdate_range(start=start_date, end=end_date).to_pydatetime().tolist()

working_days = get_working_days()


task_templates = [
    {
        "summary": "[AFX] [CMB] [CSCS] [KAS] Monitoring & Alerting from all enterprise tools",
        "description": "I monitored the customers using the following tools:\n\nRF\nPingdom\nKsiem",
        "issuetype": "Task",
        "priority": "Medium",
        "labels": ["AFX", "CMB", "CSCS", "KAS"],
        "customfield_10213": {"value": "Monitoring & Alerting"}
    },
    {
        "summary": "[AFX] [CMB] [CSCS] [KAS] Monitoring & Alerting: Manual",
        "description": "I searched for malicious domains and social media accounts impersonating my clients to carry out dubious activities on users through OSINT.",
        "issuetype": "Task",
        "priority": "Medium",
        "labels": ["AFX", "CMB", "CSCS", "KAS"],
        "customfield_10213": {"value": "Monitoring & Alerting"}
    },
    {
        "summary": "[CLAB] Avatar Management",
        "description": "I carried out my responsibility of overseeing my Avatar on Argus and made necessary updates to the logs.",
        "issuetype": "Task",
        "priority": "Low",
        "labels": ["CLAB"],
        "customfield_10213": {"value": "Threat Intelligence SecOp"}
    }
]
tasks = [
    {
        **template,  # Copy all fields from the template
        "duedate": day.strftime("%Y-%m-%d"),
        "customfield_10015": day.strftime("%Y-%m-%d"),  # Start Date
        "assignee": {"id": assignee_id}
    }
    for day in working_days
    for template in task_templates  # Create ALL templates for EACH day
]


def get_transition_id(issue_key, status_name="Done"):
    transitions = jira.transitions(issue_key)
    for t in transitions:
        if t["name"].lower() == status_name.lower():
            return t["id"]
    return None  


for task in tasks:
    new_issue = jira.create_issue(
        project="CT",  
        summary=task["summary"],
        description=task["description"],
        issuetype={"name": task["issuetype"]},
        priority={"name": task["priority"]},
        labels=task["labels"],
        assignee=task["assignee"],
        duedate=task["duedate"],
        customfield_10015=task["customfield_10015"],  
        customfield_10213=task["customfield_10213"]  
    )

    
    transition_id = get_transition_id(new_issue.key, "Done")
    if transition_id:
        jira.transition_issue(new_issue, transition_id)
        print(f"Created Task: {new_issue.key} | Status: Done | Due Date: {task['duedate']}")
    else:
        print(f"Created Task: {new_issue.key} | Could not transition to 'Done' (Check workflow)")
