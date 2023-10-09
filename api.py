import src.controller.postController as postCon
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
    return postCon.creatAssetFromConfluenceTable(companyURL,atlassianusername,apitoken,confluencePageID, atlassianworkspaceID,objektypID,listeobjectAttributesIDs,fulltable)
