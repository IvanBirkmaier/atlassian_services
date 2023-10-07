import dotenv as de
import os


de.load_dotenv()  # This will load the environment variables from .env file


# Gibt die Enviroment Variablen für ein bestimmtes Produkt zurück. Die Enviroment Variablen müssen im .env file festgelgt werden
def enviroment_variables(produkt: str):
    if produkt.lower() == "clockwork":
        CLOCKWORK_API_TOKEN = os.getenv('CLOCKWORK_API_TOKEN')
        ATLASSIAN_ACCOUNT_ID = os.getenv('ATLASSIAN_ACCOUNT_ID')
        return CLOCKWORK_API_TOKEN, ATLASSIAN_ACCOUNT_ID
    if produkt.lower() == "assets":
        COMPANY_SUBDOMAIN = os.getenv('COMPANY_SUBDOMAIN')
        USER_MAIL = os.getenv('USER_MAIL')
        JIRA_API_TOKEN = os.getenv('JIRA_API_TOKEN')
        WORKSPACE_ID = os.getenv('WORKSPACE_ID')
        return COMPANY_SUBDOMAIN, USER_MAIL, JIRA_API_TOKEN, WORKSPACE_ID
