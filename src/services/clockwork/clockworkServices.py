# Dokumentation https://docs.herocoders.com/clockwork/use-the-clockwork-api
import pandas as pd
import requests
import dotenv as de
import os


de.load_dotenv()  # This will load the environment variables from .env file

CLOCKWORK_API_TOKEN = os.getenv('CLOCKWORK_API_TOKEN')
ATLASSIAN_ACCOUNT_ID = os.getenv('ATLASSIAN_ACCOUNT_ID')

def authentification(token: str):
    header ={
        "Authorization": f"Token {token}"
    }
    return header

def createCall(clockworkEndpoint):
    # API-Endpunkt und Header-Informationen
    url = f"https://api.clockwork.report/v1/{clockworkEndpoint}"
    return url

def clockworapi(url, head):
    response = requests.get(url, headers=head)
    if response.status_code != 200:
        print("Call hat nicht geklappt")
    return response


# DEPRICATED_ Testfunktion, da warscheinlich mit Api und issueId irgendwie auch direkt möglich ist
def get_worklogs_for_ticket(accountId:str, header, url):
    response = clockworapi(url, header).json()
    ticket_worklog = []
    for res in response:
        if res["updateAuthor"]["accountId"] == accountId:
            ticket_worklog.append(res)
    return ticket_worklog

if __name__ == "__main__":
    starting_at = "2023-10-05"
    ending_at = "2023-10-06"

    endpunkt = f"worklogs?expand=worklogs&starting_at={starting_at}&ending_at={ending_at}"


    header = authentification(CLOCKWORK_API_TOKEN)
    url = createCall(endpunkt)
    ticket_worklogs = get_worklogs_for_ticket(ATLASSIAN_ACCOUNT_ID,header,url)
    tickets_worked_on = []
    manually_start = []
    manually_stop = []
    for log in ticket_worklogs:
        tickets_worked_on.append(log["issueId"])
     #################################################################################################
        # manually_start.append(log["properties"][0]["value"]["started_manually"])
        # manually_stop.append(log["properties"][0]["value"]["stopped_manually"])
     #########################################################################################
   #df = pd.DataFrame(data={"Ticket_Keys":tickets_worked_on, "start_manually": manually_start,  "stoped_manually": manually_stop})
   #count = df.groupby("Ticket_Keys").value_counts()
    print("test")
