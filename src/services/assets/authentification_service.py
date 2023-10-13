import base64

# man kann diese methode warscheinlich durch auth=HTTPBasicAuth(atlassianusername, apitoken) im request ersetzen



# Erstellt einen Auth-Header der benötigt wird um Rest-Calls an die Assets-API zu senden
# Input hierfür ist der atlassianusername: z.b ivan.birkmaier@neolern.de und ein API-Token der für den
# atlassianuser erstellt werden muss (unter folgender Adresse: https://id.atlassian.com/manage-profile/security/api-tokens)
# In der Methode wird ein Base64 Token generiert der für den Header genutzt werden muss.
def createAuthHeadersBase(atlassianusername, apitoken):
    auth = f"{atlassianusername}:{apitoken}"
    baseencoded_auth = base64.b64encode(auth.encode("utf-8")).decode("utf-8")
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Basic {baseencoded_auth}"
    }
    return headers
