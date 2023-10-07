# README #
### How do I get set up? ###
* You should set up a lokal .env file for lokally testing the implementation. The .env file needs the following variables.
  * #### Clockwork ENVs: ####
    * CLOCKWORK_API_TOKEN = "YOUR_TOKEN"
    * ATLASSIAN_ACCOUNT_ID ="YOUR_ID" (Cloud also be any other Account id)
  * #### Jira ENVs: ####
    * COMPANY_SUBDOMAIN = "COMPANY_SUBDOMAIN"
    * USER_MAIL = "YOUR_ACCOUNT_EMAIL" (Cloud also be any other Account id)
    * JIRA_API_TOKEN = "YOUR_API_TOKEN"
    * WORKSPACE_ID = "YOUR_WORKSACE_ID"
* You should also create an local_files folder where you can store your private notes for the repository or other stuff
* NOTE: Neither the .env file nor the local_files folder will ever be pushed to the remote brunch due to the .gitignore settings

### Good to know? ###
* [Learn Markdown](https://bitbucket.org/tutorials/markdowndemo)
