from jira import JIRA 
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

jira_url = os.getenv("JIRA_URL")
jira_user = os.getenv("JIRA_USER")
jira_api_token = os.getenv("JIRA_API_TOKEN")
assignee_id = os.getenv("JIRA_ASSIGNEE_ID")  

jira = JIRA(server=jira_url, basic_auth=(jira_user, jira_api_token))

# Template for sample tasks (redact or replace with your actual templates)
task_templates = [
    {
        "summary": "Task Summary 1",
        "description": "Task description goes here.",
        "issuetype": "Task",
        "priority": "Medium",
        "labels": ["LABEL1", "LABEL2"],
        "customfield_10213": {"value": "Category A"}
    },
    {
        "summary": "Task Summary 2",
        "description": "Another task description.",
        "issuetype": "Task",
        "priority": "Medium",
        "labels": ["LABEL3"],
        "customfield_10213": {"value": "Category B"}
    },
    {
        "summary": "Task Summary 3",
        "description": "Third task details here.",
        "issuetype": "Task",
        "priority": "Low",
        "labels": ["LABEL4"],
        "customfield_10213": {"value": "Category C"}
    }
]

def get_transition_id(issue_key, status_name="Done"):
    transitions = jira.transitions(issue_key)
    for t in transitions:
        if t["name"].lower() == status_name.lower():
            return t["id"]
    return None  

def create_daily_tasks():
    today = datetime.now()

    # Skip weekends
    if today.weekday() >= 5:
        print("Skipping weekend execution")
        return

    tasks = [
        {
            **template,
            "duedate": today.strftime("%Y-%m-%d"),
            "customfield_10015": today.strftime("%Y-%m-%d"),  # Start Date
            "assignee": {"id": assignee_id}
        }
        for template in task_templates
    ]

    for task in tasks:
        new_issue = jira.create_issue(
            project="PROJECT_KEY",  # Replace with your Jira project key
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

if __name__ == "__main__":
    create_daily_tasks()
