# lokal auf der Maschine: http://127.0.0.1:8000/createobject/blunexo/ivan.birkmaier@neolern.de/ATATT3xFfGF0FxxMhg3NQaotQNvmeBVL_b9KctOy_PCfLC9wDEXTtFQPIpiHxX1mllos98z0nwzEliukorkWa3RplnLhldmfe3pitbl-lVsbYsNGveE3p-Jr-Kv3hx9EhnQOGhGmjhBgbpBp2eeGja3NyYqB84wOQln_MdK80kG35O6h1wMiqCs=B0DAEA61/1361018923/35c4b64a-6d39-470f-bff7-ed56b434141b/352/3455,3458,3459/true
# lokal im Docker: http://0.0.0.0:8000//createobject/blunexo/ivan.birkmaier@neolern.de/ATATT3xFfGF0FxxMhg3NQaotQNvmeBVL_b9KctOy_PCfLC9wDEXTtFQPIpiHxX1mllos98z0nwzEliukorkWa3RplnLhldmfe3pitbl-lVsbYsNGveE3p-Jr-Kv3hx9EhnQOGhGmjhBgbpBp2eeGja3NyYqB84wOQln_MdK80kG35O6h1wMiqCs=B0DAEA61/1361018923/35c4b64a-6d39-470f-bff7-ed56b434141b/352/3455,3458,3459/true

from fastapi import FastAPI, HTTPException
import requests
from requests.auth import HTTPBasicAuth
import json
import base64
from bs4 import BeautifulSoup

app = FastAPI()
@app.get("/createobject/{companyURL}/{atlassianusername}/{apitoken}/{confluencePageID}/{atlassianworkspaceID}/{objektypID}/{listeobjectAttributesIDs}/{fulltable}")
async def create_jira_asset(
#def create_jira_asset(
        companyURL: str,
        atlassianusername: str,
        apitoken: str,
        confluencePageID: str,
        atlassianworkspaceID: str,
        objektypID: str,
        listeobjectAttributesIDs: str,
        fulltable: bool
    ):
    try:
        ###KOMMENTAR### Die Variable listeobjectAttributesIDs kann man noch Mal diskutieren, wie man eventuell es schafft, dass nicht
        # eine String-Liste an Attribut-Ids übergeben werden müssen.
        # Konvertiert den kommaseparierten String in eine Liste von IDs
        listeobjectAttributesIDs = listeobjectAttributesIDs.split(',')

        # Extrahiert den JSON-Inhalt aus der API-Antwort
        json_data = apiCall(atlassianusername, apitoken, readConfluencePage(baseUrlConfluenceApi(companyURL), confluencePageID)).json()

        # page_content zieht sich den Inhalt der Confluence Seite heraus, die in JSON-Format übergeben wurde.
        page_content = json_data['body']['storage']['value']



        ###KOMMENTAR### Die Variable projekttable kann man noch Mal diskutieren, wie man eventuell es schafft, dass nicht pauschal die letzte Tabelle einer seite genommen wird.
        # projekttable ist die letzte Tabelle auf der Confluence-Seite, wenn diese über Tabellen verfügt.
        projekttable = informationExtractor(page_content, 'table')[-1] if informationExtractor(page_content, 'table') else None
        print("test")
        print("Table", projekttable)
        print("----------------------------- Table")
        print(str(projekttable))
       ###KOMMENTAR### Dieser If abfrage kann man noch Mal diskutieren
        if fulltable:
            # rows ist eine Liste mit allen Zeilen in der Tabelle
            rows = informationExtractor(str(projekttable), 'tr') if informationExtractor(str(projekttable), 'tr') else None
        else:
            print("test")
            # Es wird sich die letzte Row der Tabelle genommen (extra als Liste konvertiert, für die später folgende Funktionalität)
            rows = [informationExtractor(str(projekttable), 'tr')[-1]] if [informationExtractor(str(projekttable), 'tr')] else []

        print("-----------------------------")
        print("rows", rows)
        # Liste mit mehreren Listen die den Tabelleninhalt abbilden (Bei Verständnisproblemen den print ausführen)
        row_content = []
        if rows:
            for row in rows:
                cells = [cell.get_text() for cell in informationExtractor(str(row), 'td')]
                if cells:
                    row_content.append(cells)
        print("row_content", row_content)

        # API-Call der Assets API für das Erstellen neuer Objekte.
        url = createCall(atlassianworkspaceID,"v1","object","create")
        # Erstellt einen Head für die Authentifizierung gegen die Jira API
        head = createAuthHeaders(atlassianusername, apitoken)

        # Durchführung der Assets-API Aufrufe um Objekte in Assets zu Erstellen
        for row in row_content:
            createJiraAssetObject(url, head, objektypID, row, listeobjectAttributesIDs)
        return {
            "status_code": 201,
            "message": "created objekts sucessfuly"
        }

    except Exception as e:
        return str(e)

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
# VARIABLE ITEM MUST BE A STRING!!!!!
def informationExtractor(item, extractor: str):
    soup = BeautifulSoup(item, 'html.parser')
    result = soup.find_all(extractor)
    print(result)
    return result

# Erstellt einen Auth-Header der benötigt wird um Rest-Calls an die Assets-API zu senden
# Input hierfür ist der atlassianusername: z.b ivan.birkmaier@neolern.de und ein API-Token der für den
# atlassianuser erstellt werden muss (unter folgender Adresse: https://id.atlassian.com/manage-profile/security/api-tokens)
# In der Methode wird ein Base64 Token generiert der für den Header genutzt werden muss.
def createAuthHeaders(atlassianusername, apitoken):
    auth = f"{atlassianusername}:{apitoken}"
    baseencoded_auth = base64.b64encode(auth.encode("utf-8")).decode("utf-8")
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Basic {baseencoded_auth}"
    }
    return headers

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

# Mit dieser Methode lasst sich ein Assets-Objekt erstellen. Hierfür muss die richtige url übergeben werden, sowie ein authentifikation-Header (head).
# Zudem muss der objekttyp, in dem das Objekt erstellt werden sollen angegeben werden. Dies geschieht über die ObjekttypID. Bei dem item  handelt es sich um eine
# Liste bsp. Person = [Karl, Johannes, 34], die die Daten representieren, aus denen ein Objekt erstellt werden soll.
# Die listeobjectAttributesIDs sind die IDs der Attribute, die im Assetsschema bereits vorhanden sein müssen (manuel angelegt oder so). Hierbei ist
# wichtig, dass diese Liste genauso lang sein muss, wie das item. Beide Listen werden nämlich dynamisch gemappt. Wenn wir in Assets zu unserem Datensatz
# Person nun das Objektschema mit der ID = 354 haben und den Attributen "Nachname" mit der ID 1, "Vorname" mit der ID 2 und "Personalnummer" mit der ID 3,
# dann muss die listeobjectAttributesIDs in folgender Reihenfolge der Methode zugeführt werden: [1, 2, 3].
# Nun geht diese Methode die Liste Person und die Liste listeobjectAttributesIDs durch und mappt jeweils beide Listen. Denn Personal[0] = "Karl" ist und
# listeobjectAttributesIDs[0] = 1 und somit die ID von Attribut Nachnamen ist, die richtigen Werte zu den richtigen Attributen.
# Abschließend wird ein REST-Call gesendet der das Objekt dann erstellt.
def createJiraAssetObject(url, head, objektypID, item, listeobjectAttributesIDs):
    print(item)
    print(listeobjectAttributesIDs)
    if len(listeobjectAttributesIDs) != len(item):
        raise Exception("Die Länge der vorgegebenen IDs muss mit der Länge von current_row_content übereinstimmen")
    attributes_list = [
        {
            "objectTypeAttributeId": str(listeobjectAttributesIDs[i]),
            "objectAttributeValues": [{"value": value}]
        }
        for i, value in enumerate(item)
    ]
    payload = json.dumps({
        "objectTypeId": objektypID,
        "attributes": attributes_list
    })
    response = requests.post(url, data=payload, headers=head)
    if response.status_code not in [200, 201]:
        raise HTTPException(status_code=response.status_code, detail="Failed to create Jira asset")

if __name__ == "__main__":
    print("start Test")
    x = create_jira_asset("blunexo", "ivan.birkmaier@neolern.de",
                            "ATATT3xFfGF0FxxMhg3NQaotQNvmeBVL_b9KctOy_PCfLC9wDEXTtFQPIpiHxX1mllos98z0nwzEliukorkWa3RplnLhldmfe3pitbl-lVsbYsNGveE3p-Jr-Kv3hx9EhnQOGhGmjhBgbpBp2eeGja3NyYqB84wOQln_MdK80kG35O6h1wMiqCs=B0DAEA61",
                            "1361018923", "35c4b64a-6d39-470f-bff7-ed56b434141b", "352", "3455,3458,3459", True)
    print("end Test")
    print(x)
