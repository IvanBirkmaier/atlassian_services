from ..services.confluence import conflueneceServices as cs
from ..services.assets import authentificationService as aut
from ..services.assets import assetsServices as asts

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
        projekttable = cs.informationExtractor(page_content, 'table', 'html.parser')[-1] if len(page_content) >= 1 else None

        ###KOMMENTAR### Dieser If abfrage kann man noch Mal diskutieren
        if fulltable:
            # rows ist eine Liste mit allen Zeilen in der Tabelle
            rows = cs.informationExtractor(str(projekttable), 'tr', 'html.parser') if len(projekttable) >= 1 else None
        else:
            # Es wird sich die letzte Row der Tabelle genommen (extra als Liste konvertiert, für die später folgende Funktionalität)
            rows = [cs.informationExtractor(str(projekttable), 'tr', 'html.parser')[-1]] if len(projekttable) >= 1 else []

        # Liste mit mehreren Listen die den Tabelleninhalt abbilden (Bei Verständnisproblemen den print ausführen)
        row_content = []
        if rows:
            for row in rows:
                cells = [cell.get_text() for cell in cs.informationExtractor(str(row), 'td', 'html.parser')] if len(row) >= 1 else []
                if cells:
                    row_content.append(cells)
        #print(row_content)

        # API-Call der Assets API für das Erstellen neuer Objekte.
        url = asts.createCall(atlassianworkspaceID, "v1", "object", "create")

        # Erstellt einen Head für die Authentifizierung gegen die Jira API
        head = aut.createAuthHeadersBase(atlassianusername, apitoken)

        # Durchführung der Assets-API Aufrufe um Objekte in Assets zu Erstellen
        for row in row_content:
            asts.createJiraAssetObject(url, head, objektypID, row, listeobjectAttributesIDs)
        return {
            "status_code": 201,
            "message": "created objekts sucessfuly"
        }
    except Exception as e:
        return str(e)

