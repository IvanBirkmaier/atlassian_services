from fastapi import HTTPException
import requests
import json

# createCall Baut einen API-Restcall zusammen um die Assets-Api anzusprechen:
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

def getObjectschemaList():
    return 0


if __name__ == "__main__":















