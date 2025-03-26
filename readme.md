# **JIRA Automation Script Documentation**  

## **Overview**  
This project automates the creation, updating, and management of JIRA issues using Python. The script is designed to:  
- Create tasks for working days within a specified timeframe.  
- Assign tasks to a specific user based on their JIRA ID.  
- Automatically transition newly created tasks to "Done" if applicable.  

## **Features**  
✅ **Automated Task Creation** – Generates tasks for working days within a given timeframe.  
✅ **Auto-Assignment** – Assigns tasks to a specific user using their JIRA ID.  
✅ **Automatic Status Transition** – Moves newly created tasks to "Done" when necessary.  

## **Prerequisites**  
Ensure you have the following installed and set up:  
- **Python 3.8+**  
- **JIRA Python Module**: Install it using:  
  ```sh
  pip install jira
  ```
- **A Valid JIRA Account**  
- **JIRA Cloud API Token** (Generate one if you don’t have it)  
- **Access to Your JIRA Project**  


## **Setup & Usage**  

### **1. Get Your JIRA User ID**  
Run the following command to retrieve your JIRA user ID:  
```sh
python id.py {find code in repo}
```
### **2**. replace placeholder with actual id in **id.py**. [Note: user ID is used to set assignee]

### **3**. Put your username in the jira search query function in **id.py**. 

### **4. Generate Your API Token**  
- Visit: **https://id.atlassian.com/manage-profile/security/api-tokens**  
- Click **Create API Token**  


