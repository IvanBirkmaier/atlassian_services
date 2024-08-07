from src.utils.utils import enviroment_variables, create_abbreviation
from src.services.assets.authentification_service import createAuthHeadersBase

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









# Dokumentieren












# DEPRICATED_ Funktion bringt keinen Mehrwert kann man auch gleich den Call einfach machen bleibt für die Übersichtlichkeit
def getObjectschemaList(url, header):
    return requests.get(url, headers=header)

def getNamelistFromObjectschema(response):
    schemas = []
    for schema in response["values"]:
        schemas.append([schema["name"], schema["objectSchemaKey"]])
    return schemas

def creatObjectSchema(name,schema_names):
    if name in schema_names:
        return False
    else:
        return name

# Mit dieser
def checkRequiredValues(existing_schemata: list, slicer: int, value_to_check= ""):
    itemlist = []
    for schema in existing_schemata:
        itemlist.append(schema[slicer])
    if value_to_check != "":
        return creatObjectSchema(value_to_check,itemlist), itemlist
    else:
        return False, itemlist

def createObjectschema(head ,url, name,abbreviation,description):
    payload = json.dumps({
        "name":name,
        "objectSchemaKey": abbreviation,
        "description": description
    })
    return requests.post(url, data=payload, headers=head)





if __name__ == "__main__":
    ########################### Schema Variablen #########################################
    objectSchema_name = "AA_Test"
    description = "Testschema angelget durch Api"
    ################### API-Variablen #####################################
    typeClass = "objectschema"
    atlassianEndpoint_list = "list"
    atlassianEndpoint_create = "create"
    version = "v1"
    COMPANY_SUBDOMAIN, USER_MAIL, JIRA_API_TOKEN, WORKSPACE_ID = enviroment_variables("assets")
    ##################################### Logik ############################################
    url = createCall(WORKSPACE_ID,version,typeClass,atlassianEndpoint_list)
    response = getObjectschemaList(url, createAuthHeadersBase(USER_MAIL, JIRA_API_TOKEN)).json()
    schemas = getNamelistFromObjectschema(response)
    schema_name, _= checkRequiredValues(schemas,0,objectSchema_name)
    _, abbreviation_list= checkRequiredValues(schemas,1)

    if schema_name:
        abbreviation = create_abbreviation(schema_name, abbreviation_list)
        url = createCall(WORKSPACE_ID, version, typeClass, atlassianEndpoint_create)
        response = createObjectschema(createAuthHeadersBase(USER_MAIL, JIRA_API_TOKEN) ,url, schema_name,abbreviation,description)
        if response.status_code not in [200, 201]:
            print()
            raise HTTPException(status_code=response.status_code, detail="Failed to create Jira asset")
    print("test")














