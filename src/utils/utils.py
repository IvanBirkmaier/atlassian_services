from bs4 import BeautifulSoup
import os
import itertools
import re
import string as st
import dotenv as de

# This will load the environment variables from .env file
de.load_dotenv()



'''
DESCRIPTION:
This methode returns the enviroment variables which have to be set in an .env file at the rootlevel of this respository.
For this script you have to install dotenv-package in your python-enviroment. For getting the right result you have to name your
enviroment variables in the your .env file as written in for example in os.getenv('CLOCKWORK_API_TOKEN').
-------------------------------------------------------------------------------------------
INPUT:
produkt: String with the atlassian Produkt for which you need the env-variables
-------------------------------------------------------------------------------------------
RETURN: Every env-variable as string
-------------------------------------------------------------------------------------------
NOTE:
Aways make sure that the .env file is set in your .gitignore file so that your personal information will never be pushed to any
remote brunch. This is to make sure that there is no possibilty to spread your personal information trough the internet.
'''
def enviroment_variables(produkt: str):
    if produkt.lower() == "atlassian":
        COMPANY_SUBDOMAIN = os.getenv('COMPANY_SUBDOMAIN')
        USER_MAIL = os.getenv('USER_MAIL')
        ATLASSIAN_API_TOKEN = os.getenv('ATLASSIAN_API_TOKEN')
        WORKSPACE_ID = os.getenv('WORKSPACE_ID')
        return COMPANY_SUBDOMAIN, USER_MAIL, ATLASSIAN_API_TOKEN, WORKSPACE_ID
    if produkt.lower() == "clockwork":
        CLOCKWORK_API_TOKEN = os.getenv('CLOCKWORK_API_TOKEN')
        ATLASSIAN_ACCOUNT_ID = os.getenv('ATLASSIAN_ACCOUNT_ID')
        return CLOCKWORK_API_TOKEN, ATLASSIAN_ACCOUNT_ID
    # For the test in file dict = src.test.utils.utils.
    if produkt.lower() == "test":
        TEST_API_TOKEN = "12345Token"
        TEST_USER_ID = "max.mustermann@test.com"
        return TEST_API_TOKEN, TEST_USER_ID


'''
DESCRIPTION:
Creates an abbreviation from a giving string by comparing the created abbreviation to a list of already existing abbreviation. If the abbreviation already exist in the given list
then the funktion modifies the created abbreviation until it created an uique abbreviation for the given string.
Example: 
  string = "TestString" (initial expected abbreviation = "TE"
  existing_abbreviations = ["AB","TE"]
Because the initial abbreviation is already existing in the list of given abbreviation exist, the methode returns "TES". 
Otherwise the methode whould return "TE".
-------------------------------------------------------------------------------------------
INPUT:
string = String for which you would like to get the abbreviations
existing_abbreviations = List of strings with existing abbreviations (also empty list is possible)
-------------------------------------------------------------------------------------------
RETURN:
abbreviation = Stirng with abbreviation
'''
def create_abbreviation(string: str, existing_abbreviations: list):
    string = re.sub("[^a-zA-ZäöüÄÖÜß ]", "", string)
    if string and len(string) > 1:
        # Split the string at spaces if spaces existing otherwise split ist just a list of with the string
        splits = string.upper().split()
        # Takes the list split, iterates throug it and joins the first letter of every item in the list uppercase.
        # If split only consist of one item /word then abbreviation has only one letter and is to short
        abbreviation = ''.join([split[0] for split in splits if split])
        # If the abbreviation is only one character, use the second character of the first word part adds it to the abbreviation
        if len(abbreviation) == 1:
            abbreviation += splits[0][1]
        # sets i on length of abbreviation (=2) for later check.
        i = len(abbreviation)
        all_chars = ''.join(splits)
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
    else:
        length = 2
        while True:
            # Creates all possible combinations for the current length
            all_combinations = [''.join(comb) for comb in itertools.product(st.ascii_uppercase, repeat=length)]
            # Finds the first combination not in the existing list
            for abbreviation in all_combinations:
                if abbreviation not in existing_abbreviations:
                    return abbreviation
            # Increases the length for the combinations to be generated
            length += 1


'''
DESCRIPTION:
This function can extract information from HTML-page/content. It takes the content (f.e. HTML-page, or any other subset of HTML-tags) and extract the given
content for the given extractor: For example content is an HTML page with two tables on it <table>. If we set extractor = "table" then the returned result 
will be a ResultSet with the entries of the type SoupStrainer (both from BeautifulSoup) of the two tables from the page. This function needs also an parser. The libeary which is used for extracting the content is Beautiful Soup.
Beautiful soup provieds a set of parser. 
-------------------------------------------------------------------------------------------
INPUT:
content = HTML-Page, or subset
extractor = HTML-Element which you want to be extracted
parser = Can be one of: 'html.parser', 'lxml', 'lxml-xml', 'html5lib'
-------------------------------------------------------------------------------------------
RETURN:
result = will be a ResultSet with the entries of the type SoupStrainer (both from BeautifulSoup)
-------------------------------------------------------------------------------------------
NOTE: With the methode .get_text from BeautifulSoup you can acess the text value of the extracted HTML elements 
'''
def information_extractor(content:str, extractor: str, parser: str):
    soup = BeautifulSoup(content, parser)
    result = soup.find_all(extractor)
    return result

