# Atlassian Services

## Description

This repository interacts with the Atlassian API to implement various workflows. The key workflows included in this project are:

1. **Workflow 1**: Reading from a Confluence page and creating asset objects.
2. **Workflow 2**: Extracting information from Clockwork.

### How do I get set up?

To set up the project locally for testing, you need to configure a `.env` file with the following variables:

#### Clockwork ENVs:
```bash
CLOCKWORK_API_TOKEN = "YOUR_TOKEN"
ATLASSIAN_ACCOUNT_ID = "YOUR_ID" # Could also be any other Account ID
```

#### Jira ENVs:
```bash
COMPANY_SUBDOMAIN = "COMPANY_SUBDOMAIN"
USER_MAIL = "YOUR_ACCOUNT_EMAIL" # Could also be any other Account ID
JIRA_API_TOKEN = "YOUR_API_TOKEN"
WORKSPACE_ID = "YOUR_WORKSPACE_ID"
```

Additionally, create a `local_files` folder to store your private notes or other relevant files. Note that neither the `.env` file nor the `local_files` folder will be pushed to the remote branch due to the `.gitignore` settings.

## Tech Stack

The main technologies used in this project are:

- Docker
- FastAPI
- Atlassian Python API
