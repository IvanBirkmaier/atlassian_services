import dotenv as de
# This will load the environment variables from .env file
de.load_dotenv()
import os


'''
This methode returns the enviroment variables which have to be set in an .env file at the rootlevel of this respository.
For this script you have to install dotenv-package in your python-enviroment. For getting the right result you have to name your
enviroment variables in the your .env file as written in for example in os.getenv('CLOCKWORK_API_TOKEN').

NOTE:
Aways make sure that the .env file is set in your .gitignore file so that your personal information will never be pushed to any
remote brunch. This is to make sure that there is no possibilty to spread your personal information trough the internet.
'''
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
    # For the test in file dict = src.test.utils.utils.
    if produkt.lower() == "test":
        TEST_API_TOKEN = "12345Token"
        TEST_USER_ID = "max.mustermann@test.com"
        return TEST_API_TOKEN, TEST_USER_ID

'''
Creates an abbreviation from a giving string by comparing the created abbreviation to a list of already existing abbreviation. If the abbreviation already exist in the given list
then the funktion modifies the created abbreviation until it created an uique abbreviation for the given string.
Example: 
  string = "TestString" (initial expected abbreviation = "TE"
  existing_abbreviations = ["AB","TE"]
Because the initial abbreviation is already existing in the list of given abbreviation exist, the methode returns "TES". 
Otherwise the methode whould return "TE".
'''
def create_abbreviation(string: str, existing_abbreviations: list):
    # Split the string at spaces if spaces existing otherwise split ist just a list of with the string
    splits = string.split()
    # Creates a
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


# Diese Method nimmt ein String (Wort) entgegen und gibt ein Kürzel-Zurück

# def create_abbreviation(string: str, existing_abbreviations: list):
#     splits = string.split('_')  # Split the word at underscores
#     abbreviation = ''.join([split[0].upper() for split in splits if split])
#
#     # Add characters to the abbreviation until it's unique or all characters are used
#     i = 1
#     all_chars = ''.join(splits).upper()
#     while abbreviation in existing_abbreviations and i < len(all_chars):
#         abbreviation += all_chars[i]
#         i += 1
#
#     # If we've used up all characters and the abbreviation is still not unique, add numbers
#     number = 1
#     while abbreviation in existing_abbreviations:
#         abbreviation = abbreviation[:-1] if number > 1 else abbreviation  # remove the previous number
#         abbreviation += str(number)
#         number += 1
#
#     return abbreviation