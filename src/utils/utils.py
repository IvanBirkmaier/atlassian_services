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

# Diese Method nimmt ein String (Wort) entgegen und gibt ein Kürzel-Zurück

def create_abbreviation(string: str, existing_abbreviations: list):
    splits = string.split('_')  # Split the word at underscores
    abbreviation = ''.join([split[0].upper() for split in splits if split])

    # Add characters to the abbreviation until it's unique or all characters are used
    i = 1
    all_chars = ''.join(splits).upper()
    while abbreviation in existing_abbreviations and i < len(all_chars):
        abbreviation += all_chars[i]
        i += 1

    # If we've used up all characters and the abbreviation is still not unique, add numbers
    number = 1
    while abbreviation in existing_abbreviations:
        abbreviation = abbreviation[:-1] if number > 1 else abbreviation  # remove the previous number
        abbreviation += str(number)
        number += 1

    return abbreviation


def create_abbreviation(string: str, existing_abbreviations: list):
    splits = string.split()  # Split the word at spaces
    abbreviation = ''.join([split[0].upper() for split in splits if split])

    # If the abbreviation is only one character, use the second character of the first word part
    if len(abbreviation) == 1:
        abbreviation += splits[0][1].upper()

    all_chars = ''.join(splits).upper()
    i = len(abbreviation)

    # Add characters to the abbreviation until it's unique or all characters are used
    while abbreviation in existing_abbreviations and i < len(all_chars):
        abbreviation += all_chars[i]
        i += 1

    # If we've used up all characters and the abbreviation is still not unique, repeat the characters
    char_index = 0
    while abbreviation in existing_abbreviations:
        abbreviation += all_chars[char_index % len(all_chars)]
        char_index += 1

    return abbreviation
