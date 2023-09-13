from requests.auth import HTTPBasicAuth
from fastapi import HTTPException
from bs4 import BeautifulSoup
import requests


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

# Diese Methode holt sich die Informationen, eines Items, dass über die Variable item in die Methode eingegeben wird.
# Sprich wenn es sich bei dem Item um eine Liste handelt [<h1>Hello World ist</h1>, <p>Test</p>] und der wird auf extractor = 'h1',
# dann ist die Variable result die zurückgegeben wird [<h1>Hello World ist</h1>]. TIPP: wenn nach dem Methodenaufruf die
# BeautifulSoup-Methode .get_text() hintuzgefgt wird dann lässt sich nur der Text des gewählten extraktors ausgeben. Sprich
# result = 'Hello World'.
# BOTH VARIABLEs MUST BE A STRING!!!!!
def informationExtractor(item: str, extractor: str):
    soup = BeautifulSoup(item, 'html.parser')
    result = soup.find_all(extractor)
    return result


