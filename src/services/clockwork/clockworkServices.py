# Dokumentation https://docs.herocoders.com/clockwork/use-the-clockwork-api
import pandas as pd
import requests
import pandas

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
    api_token = "3km31746G/4twG2/BZj6KPWA35+t+c1lJ3NCCg3p6VMpo5vK2xyxDdYo8zFJoDUyMMBGRyYHQef6a7eQPThydNCYYnKSHEdI8hPx/Q==--07v6lPkTJNyXMhR/--SewUbFOiyAI/2+8NnjWdCQ=="
    accountId ="624c31d37a3f9e006ab5ab30" # Ivan Birkmaier
    accountId ="5e41c799a17f930c9b93efdc" # Thorsten Hahn
    accountId = "712020:f7804a87-0873-48b0-869b-299f040495c9" #Arash
    starting_at = "2023-10-05"
    ending_at = "2023-10-06"

    # Alle worklogs, aller tickets vom user mit der account_id die bis zum 05.10.2023 geschlossenm wurden
    # endpunkt = "worklogs?expand=worklogs&ending_at=2023-10-06&account_id=624c31d37a3f9e006ab5ab30"

    # Alle worklogs, aller tickets vom user mit der account_id die am 05.10.2023 angefangen wurden und am 05.10.2023 wieder geschlossenm wurden
    # endpunkt = "worklogs?expand=worklogs&ending_at=2023-10-05&account_id=624c31d37a3f9e006ab5ab30&starting_at=2023-10-05"

    #endpunkt = "worklogs?expand=worklogs&ending_at=2023-09-28&account_id=624c31d37a3f9e006ab5ab30&starting_at=2023-09-28"

    # endpunkt = "worklogs?expand=worklogs&ending_at=2023-10-05&account_id=624c31d37a3f9e006ab5ab30&starting_at=2023-09-27"

    endpunkt = f"worklogs?expand=worklogs&starting_at={starting_at}&ending_at={ending_at}"


    header = authentification(api_token)
    url = createCall(endpunkt)
    ticket_worklogs = get_worklogs_for_ticket(accountId,header,url)
    tickets_worked_on = []
    manually_start = []
    manually_stop = []
    for log in ticket_worklogs:
        tickets_worked_on.append(log["issueId"])
     #################################################################################################
        # manually_start.append(log["properties"][0]["value"]["started_manually"])
        # manually_stop.append(log["properties"][0]["value"]["stopped_manually"])
     #########################################################################################
   # df = pd.DataFrame(data={"Ticket_Keys":tickets_worked_on, "start_manually": manually_start,  "stoped_manually": manually_stop})
    # count = df.groupby("Ticket_Keys").value_counts()
    print("test")
