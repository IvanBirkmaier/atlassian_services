# lokal auf der Maschine: http://127.0.0.1:8000/createobject/blunexo/ivan.birkmaier@neolern.de/ATATT3xFfGF0FxxMhg3NQaotQNvmeBVL_b9KctOy_PCfLC9wDEXTtFQPIpiHxX1mllos98z0nwzEliukorkWa3RplnLhldmfe3pitbl-lVsbYsNGveE3p-Jr-Kv3hx9EhnQOGhGmjhBgbpBp2eeGja3NyYqB84wOQln_MdK80kG35O6h1wMiqCs=B0DAEA61/1361018923/35c4b64a-6d39-470f-bff7-ed56b434141b/352/3455,3458,3459/true

import src.controller.getController as getCon
from fastapi import FastAPI

app = FastAPI()


@app.get("/createobject/{companyURL}/{atlassianusername}/{apitoken}/{confluencePageID}/{atlassianworkspaceID}/{objektypID}/{listeobjectAttributesIDs}/{fulltable}")
async def create_jira_asset(
        companyURL: str,
        atlassianusername: str,
        apitoken: str,
        confluencePageID: str,
        atlassianworkspaceID: str,
        objektypID: str,
        listeobjectAttributesIDs: str,
        fulltable: bool
):
    print(companyURL)
    return getCon.creatAssetFromConfluenceTable(companyURL,atlassianusername,apitoken,confluencePageID, atlassianworkspaceID,objektypID,listeobjectAttributesIDs,fulltable)
