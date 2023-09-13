# lokal auf der Maschine: http://127.0.0.1:8000/createobject/blunexo/ivan.birkmaier@neolern.de/ATATT3xFfGF0FxxMhg3NQaotQNvmeBVL_b9KctOy_PCfLC9wDEXTtFQPIpiHxX1mllos98z0nwzEliukorkWa3RplnLhldmfe3pitbl-lVsbYsNGveE3p-Jr-Kv3hx9EhnQOGhGmjhBgbpBp2eeGja3NyYqB84wOQln_MdK80kG35O6h1wMiqCs=B0DAEA61/1361018923/35c4b64a-6d39-470f-bff7-ed56b434141b/352/3455,3458,3459/true
# lokal im Docker: http://0.0.0.0:8000//createobject/blunexo/ivan.birkmaier@neolern.de/ATATT3xFfGF0FxxMhg3NQaotQNvmeBVL_b9KctOy_PCfLC9wDEXTtFQPIpiHxX1mllos98z0nwzEliukorkWa3RplnLhldmfe3pitbl-lVsbYsNGveE3p-Jr-Kv3hx9EhnQOGhGmjhBgbpBp2eeGja3NyYqB84wOQln_MdK80kG35O6h1wMiqCs=B0DAEA61/1361018923/35c4b64a-6d39-470f-bff7-ed56b434141b/352/3455,3458,3459/true

from ..services.confluence import conflueneceServices as cs
from ..services.jira import authentificationService as aut
from ..services.jira import assetsServices as asts

def creatAssetFromConfluenceTable(
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
        # Konvertiert den kommaseparierten String in eine Liste von IDs
        listeobjectAttributesIDs = listeobjectAttributesIDs.split(',')

        # Extrahiert den JSON-Inhalt aus der API-Antwort
        json_data = cs.apiCall(atlassianusername, apitoken, cs.readConfluencePage(cs.baseUrlConfluenceApi(companyURL), confluencePageID)).json()

        # page_content zieht sich den Inhalt der Confluence Seite heraus, die in JSON-Format übergeben wurde.
        page_content = json_data['body']['storage']['value']

        ###KOMMENTAR### Die Variable projekttable kann man noch Mal diskutieren, wie man eventuell es schafft, dass nicht pauschal die letzte Tabelle einer seite genommen wird.
        # projekttable ist die letzte Tabelle auf der Confluence-Seite, wenn diese über Tabellen verfügt.
        projekttable = cs.informationExtractor(page_content, 'table')[-1] if cs.informationExtractor(page_content,'table') else None

        ###KOMMENTAR### Dieser If abfrage kann man noch Mal diskutieren
        if fulltable:
            # rows ist eine Liste mit allen Zeilen in der Tabelle
            rows = cs.informationExtractor(str(projekttable), 'tr') if cs.informationExtractor(str(projekttable), 'tr') else None
        else:
            # Es wird sich die letzte Row der Tabelle genommen (extra als Liste konvertiert, für die später folgende Funktionalität)
            rows = [cs.informationExtractor(str(projekttable), 'tr')[-1]] if cs.informationExtractor(str(projekttable), 'tr') else []

        # Liste mit mehreren Listen die den Tabelleninhalt abbilden (Bei Verständnisproblemen den print ausführen)
        row_content = []
        if rows:
            for row in rows:
                cells = [cell.get_text() for cell in cs.informationExtractor(str(row), 'td')]
                if cells:
                    row_content.append(cells)
        #print(row_content)

        # API-Call der Assets API für das Erstellen neuer Objekte.
        url = asts.createCall(atlassianworkspaceID, "v1", "object", "create")

        # Erstellt einen Head für die Authentifizierung gegen die Jira API
        head = aut.createAuthHeaders(atlassianusername, apitoken)

        # Durchführung der Assets-API Aufrufe um Objekte in Assets zu Erstellen
        for row in row_content:
            asts.createJiraAssetObject(url, head, objektypID, row, listeobjectAttributesIDs)
        return {
            "status_code": 201,
            "message": "created objekts sucessfuly"
        }
    except Exception as e:
        return str(e)

