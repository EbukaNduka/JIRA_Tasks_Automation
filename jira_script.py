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
    start_date = datetime(year, 1, 1)
    end_date = datetime(year, 3, 31)  

    
    business_days = pd.bdate_range(start=start_date, end=end_date).to_pydatetime().tolist()

    return business_days[:60]  


working_days = get_working_days()


tasks = [
    {
        "summary": "",
        "description": "",
        "issuetype": "",
        "priority": "",
        "duedate": working_days[i].strftime("%Y-%m-%d"),  
        "labels": [""],
        "assignee": {"id": "assignee_id"},  
        "customfield_10213": {"value": ""},  # Category (Custom Field)
        "customfield_10015": working_days[i].strftime("%Y-%m-%d")  # Start Date (Custom Field)
    }
    for i in range(60)  
]


def get_transition_id(issue_key, status_name="Done"):
    transitions = jira.transitions(issue_key)
    for t in transitions:
        if t["name"].lower() == status_name.lower():
            return t["id"]
    return None  


for task in tasks:
    new_issue = jira.create_issue(
        project="",  
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
