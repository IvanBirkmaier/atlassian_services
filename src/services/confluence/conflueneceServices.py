from requests.auth import HTTPBasicAuth
from fastapi import HTTPException
import requests

'''
This function creates/returns an base Url for any api-call with the confluence api from atlassian.
company_subdomain = The companie subdomain provided by atlassian.
'''
def base_url_confluence_api(company_subdomain):
    BASE_URL = f"https://{company_subdomain}.atlassian.net/wiki/rest/api"
    return BASE_URL


'''
This function creates/returns the api call with the endpoint for getting the contend of an confluence page.
base_url = Base url which is needed for any apicall with the confluence api.
confluence_page_id = Page id from confluence for reading a page.
'''
def endpoint_get_pagecontent(base_url, confluence_page_id):
    url = f"{base_url}/content/{confluence_page_id}?expand=body.storage"
    return url


'''
This function runs an request.get api call for a given url for the call. If the HTTP status code of the response is 200
then it returns the response of the call. By any other  HTTP status code (f.e. 404, 405) it raises an HTTPException.
USER_MAIL: Mailadresse of atlassian user
ATLASSIAN_API_TOKEN: Self generated api token. (NOTE its always the token of your account and you need to have the right acces rights)
call_url: The url for the api call.
'''
def get_api_call(USER_MAIL, ATLASSIAN_API_TOKEN, call_url):
    response = requests.get(call_url, auth=HTTPBasicAuth(USER_MAIL, ATLASSIAN_API_TOKEN))
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Failed to get page content")
    return response
