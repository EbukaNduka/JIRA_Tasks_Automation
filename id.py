from jira import JIRA 
import os
from dotenv import load_dotenv


load_dotenv()


jira_url = os.getenv("JIRA_URL")
jira_user = os.getenv("JIRA_USER")
jira_api_token = os.getenv("JIRA_API_TOKEN")


jira = JIRA(server=jira_url, basic_auth=(jira_user, jira_api_token))
user = jira.search_users(query="")[0]  #Put your username in the jira search query function
print(f"User ID: {user.accountId}")  
