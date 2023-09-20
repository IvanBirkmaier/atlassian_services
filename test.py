from fastapi import FastAPI, HTTPException
import requests
from requests.auth import HTTPBasicAuth
import json
import base64
from bs4 import BeautifulSoup

# Funktion zu Erstelllung einer Basis-URL die benötigt wird um Api-Calls mit der Confluence API durchzuführen
# companyURL: Das Unternehmenskürzel unserer Atlassian-Subdomaine
def baseUrlConfluenceApi(companyURL):
    # Basis-URL für Confluence API
    BASE_URL = f"https://{companyURL}.atlassian.net/wiki/rest/api"
    return BASE_URL

# Baut den Endpunkt, der dafür benötigt wird, um eine Confluence-Seite komplett auszulesen.
# baseURl: Basis URl aus dem authentification.py Service Script.
# confluencePageID: Id der Confluence Seite die ausgelesen werden soll.
def readConfluencePage(baseUrl, confluencePageID):
    # Endpunkt für den Confluence API-Aufruf (Confluence Seite auslesen)
    url = f"{baseUrl}/content/{confluencePageID}?expand=body.storage"
    return url

def getContentTemplate(baseUrl):
    url = f"https://{baseUrl}/template/page"
    return url




# apiCall ist eine Methode die einen apiCall an die Confluence-Api durchführt. Um diesen Call durchführen zu können benötigt die
# methode die drei Variablen, atlassianusername (E-Mail eines Atlassian Users) den dazu gehörigen API-Token und eine
# Url für den API-Call wie z.b. in der Methode readpage erstellt.
def apiCall(atlassianusername, apitoken, urlForCall):
    # API-Aufruf an Confluence
    response = requests.get(urlForCall, auth=HTTPBasicAuth(atlassianusername, apitoken))
    # Überprüfung des API-Statuscodes (Wenn erfolgreich, dann Status 200 und Script geht weiter. Wenn erfogreich dann springt das Script an der stelle raus)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Failed to get page content")
    # Extrahiert den JSON-Inhalt aus der API-Antwort
    return response

def apiCall2(atlassianusername, apitoken, urlForCall):
    headers = {
        "Accept": "application/json"
    }
    # API-Aufruf an Confluence
    response = requests.get(urlForCall, headers=headers, auth=HTTPBasicAuth(atlassianusername, apitoken), timeout=10)
    # Überprüfung des API-Statuscodes (Wenn erfolgreich, dann Status 200 und Script geht weiter. Wenn erfogreich dann springt das Script an der stelle raus)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Failed to get page content")
    # Extrahiert den JSON-Inhalt aus der API-Antwort
    return response

# Diese Methode holt sich die Informationen, eines Items, dass über die Variable item in die Methode eingegeben wird.
# Sprich wenn es sich bei dem Item um eine Liste handelt [<h1>Hello World ist</h1>, <p>Test</p>] und der wird auf extractor = 'h1',
# dann ist die Variable result die zurückgegeben wird [<h1>Hello World ist</h1>]. TIPP: wenn nach dem Methodenaufruf die
# BeautifulSoup-Methode .get_text() hintuzgefgt wird dann lässt sich nur der Text des gewählten extraktors ausgeben. Sprich
# result = 'Hello World'.
# VARIABLE ITEM MUST BE A STRING!!!!!
def informationExtractor(item, extractor: str, parser: str):
    if not isinstance(item, str):
        raise TypeError(f"Die übergebene Variable item muss für die Methode informationExtractor() ein String sein. Möglich mit str(item) beim übergeben in die Methode")
    soup = BeautifulSoup(item, parser)
    result = soup.find_all(extractor)
    print(result)
    return result

# Baut einen API-Restcall zusammen um die Assets-Api anzusprechen:
# version: ist die Version die derzeit von Atlassian angeboten wird
# typeClass: simboliesiert die Kategorien die Atlassian bei ihrer Dokumentation zur verfügung stellt (zb. /objekt)
#atlassianEndpoint: Ist der von Atlassian zur Verfügung gestellter Endpoint
# atlassianworkspaceID: Ist die von Atlassian bereitgestellte WorkspaceID zu finden unter der folgendne URL (https://blunexo.atlassian.net/rest/servicedeskapi/assets/workspace)
# So lassen sich selbständig Api-Calls zusammenbauen und müssen nicht hardgecoded werden.
# z.B: https://api.atlassian.com/jsm/assets/workspace/{atlassianworkspaceID}/v1/object/create
def createCall(atlassianworkspaceID,version,typeClass,atlassianEndpoint):
    # API-Endpunkt und Header-Informationen
    url = f"https://api.atlassian.com/jsm/assets/workspace/{atlassianworkspaceID}/{version}/{typeClass}/{atlassianEndpoint}"
    return url


def testExtractACBYTitle(projekttable):
    for ac in projekttable:
        table = informationExtractor(str(ac), 'ac:parameter', 'html.parser')[0].get_text()  if informationExtractor(str(ac),'ac:parameter', 'html.parser') else None
        if table == "test":
            return ac

if __name__ == "__main__":
    # lokal auf der Maschine: http://127.0.0.1:8000/createobject/blunexo/ivan.birkmaier@neolern.de/ATATT3xFfGF0FxxMhg3NQaotQNvmeBVL_b9KctOy_PCfLC9wDEXTtFQPIpiHxX1mllos98z0nwzEliukorkWa3RplnLhldmfe3pitbl-lVsbYsNGveE3p-Jr-Kv3hx9EhnQOGhGmjhBgbpBp2eeGja3NyYqB84wOQln_MdK80kG35O6h1wMiqCs=B0DAEA61/1361018923/35c4b64a-6d39-470f-bff7-ed56b434141b/352/3455,3458,3459/true
    companyURL = "blunexo"
    atlassianusername = "ivan.birkmaier@neolern.de"
    apitoken = "ATATT3xFfGF0FxxMhg3NQaotQNvmeBVL_b9KctOy_PCfLC9wDEXTtFQPIpiHxX1mllos98z0nwzEliukorkWa3RplnLhldmfe3pitbl-lVsbYsNGveE3p-Jr-Kv3hx9EhnQOGhGmjhBgbpBp2eeGja3NyYqB84wOQln_MdK80kG35O6h1wMiqCs=B0DAEA61"
    confluencePageID = "1361018923"

    # Extrahiert den JSON-Inhalt aus der API-Antwort
    json_data = apiCall(atlassianusername, apitoken, readConfluencePage(baseUrlConfluenceApi(companyURL), confluencePageID)).json()

    # Call 2 get all contenttemplates
    #print(json.dumps(json.loads(apiCall2(atlassianusername, apitoken, getContentTemplate(baseUrlConfluenceApi(companyURL))).text), sort_keys=True, indent=4, separators=(",", ": ")))

    #page_content zieht sich den Inhalt der Confluence Seite heraus, die in JSON-Format übergeben wurde.
    page_content = json_data['body']['storage']['value']

    ###KOMMENTAR### Die Variable projekttable kann man noch Mal diskutieren, wie man eventuell es schafft, dass nicht pauschal die letzte Tabelle einer seite genommen wird.
    #projekttable ist die letzte Tabelle auf der Confluence-Seite, wenn diese über Tabellen verfügt.
    projekttable = informationExtractor(page_content, 'ac:structured-macro', 'html.parser') if informationExtractor(page_content,'ac:structured-macro', 'html.parser') else None
    x = testExtractACBYTitle(projekttable)
    y = informationExtractor(x, "h1", "html.parser")[0].get_text()

    print(x)