from src.services.confluence import confluenece_services as cs

# Script_variables
TEST_RUNS_test_base_url_confluence_api = ["test", ["Second_Test", "SE", ["AB", "TI"]],111,1.312,]
TEST_RUNS_test_endpoint_get_pagecontent = [["test", 111], ["test"]]

# cs.endpoint_get_pagecontent()

# cs.get_api_call()


'''
This test function tests the returns of the function test_base_url_confluence_api for diffrent inputs define in
script variable TEST_RUNS_test_base_url_confluence_api. 
-------------------------------------------------------------------------------------------
FUNCTION WHICH IS TESTED:
base_url_confluence_api()
'''
def test_base_url_confluence_api():
    company_subdomain = TEST_RUNS_test_base_url_confluence_api.pop(0)
    expected_base_url = f"https://{company_subdomain}.atlassian.net/wiki/rest/api"
    returned_base_url = cs.base_url_confluence_api(company_subdomain)
    while TEST_RUNS_test_base_url_confluence_api:
        if expected_base_url == returned_base_url:
            if type(expected_base_url) == type(returned_base_url):
                test_base_url_confluence_api()
            else:
                raise AssertionError(f"Expected type of the excpected bas url {type(expected_base_url)}, but received type: {type(returned_base_url)}.")
        else:
            raise AssertionError(f"Expected abbreviation {expected_base_url}, but received {returned_base_url}.")
    assert expected_base_url == returned_base_url

'''
This test function tests the returns of the function test_base_url_confluence_api for diffrent inputs define in
script variable TEST_RUNS_test_base_url_confluence_api. 
-------------------------------------------------------------------------------------------
FUNCTION WHICH IS TESTED:
endpoint_get_pagecontent()
'''
def test_endpoint_get_pagecontent():
    company_subdomain = TEST_RUNS_test_base_url_confluence_api.pop(0)
    expected_base_url = f"https://{company_subdomain}.atlassian.net/wiki/rest/api"
    returned_base_url = cs.base_url_confluence_api(company_subdomain)
    while TEST_RUNS_test_base_url_confluence_api:
        if expected_base_url == returned_base_url:
            if type(expected_base_url) == type(returned_base_url):
                test_base_url_confluence_api()
            else:
                raise AssertionError(f"Expected type of the excpected bas url {type(expected_base_url)}, but received type: {type(returned_base_url)}.")
        else:
            raise AssertionError(f"Expected abbreviation {expected_base_url}, but received {returned_base_url}.")
    assert expected_base_url == returned_base_url
