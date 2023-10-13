from bs4 import BeautifulSoup, ResultSet, Tag
from src.utils import utils as utl

# Script_variables:
TEST_RUNS_test_create_abbreviation = [["Second_Test", "SE", ["AB", "TI"]], ["thridTest", "THR", ["AB", "TH"]],
                                      ["A", "AA", ["AB", "TI"]], ["fifth test", "FTF", ["AB", "FT"]],
                                      ["$4 444", "AA", ["AB", "FT"]], ["$4 444", "AC", ["AB", "FT", "AA"]],
                                      ["$4 444", "AD", ["AB", "FT", "AA", "AC"]]]

TEST_RUNS_test_information_extractor = [
    ["<html><th>Second Test</th></html>", "th", [["th", "Second Test"]], "html.parser"],
    ["<h1><p>Third Test a</p><p>Third Test b</p><p>Third Test c</p></h1>", "p",
     [["p", "Third Test a"], ["p", "Third Test b"], ["p", "Third Test c"]], "html.parser"],
    ["<table><tbody><tr>Unit Test</tr></tbody></table>", "tbody", [["tbody", "<tr>Unit Test</tr>"]], "html.parser"]]

'''
DESCRIPTION:
This is an recrusiv test-methode where multiple test runs, which are defined in the Script_variables. It tests the methode of. 
Teste methode: create_abbreviation
-------------------------------------------------------------------------------------------
FUNCTION WHICH IS TESTED:
create_abbreviation(string, existing_abbreviations)
'''
def test_create_abbreviation(string="Initial Test", abbreviation="IT", existing_abbreviations=["AB", "TI"]):
    # Get the abbreviation from the method.
    abbreviation_from_method = utl.create_abbreviation(string, existing_abbreviations)
    # Check if the expected abbreviation matches the abbreviation returned by the method.
    if abbreviation == abbreviation_from_method:
        # Check if there's still a run left in the Script_variable.
        if TEST_RUNS_test_create_abbreviation:
            # If a run remains, take that run and remove it from the list of runs.
            run = TEST_RUNS_test_create_abbreviation.pop(0)
            # Execute the same method with the new run from all the test runs.
            test_create_abbreviation(run[0], run[1], run[2])
        # If this method executes up to here, the test is complete.
        assert abbreviation == abbreviation_from_method
    else:
        raise AssertionError(f"Expected abbreviation {abbreviation}, but received {abbreviation_from_method}.")


'''
This test function tests the returns of the function enviroment_variables for the "test" input. 
-------------------------------------------------------------------------------------------
FUNCTION WHICH IS TESTED:
enviroment_variables(product)
'''
def test_enviroment_variables():
    EXPECTED_OUTPUT_TEST_API_TOKEN = "12345Token"
    EXPECTED_OUTPUT_TEST_USER_ID = "max.mustermann@test.com"
    TEST_API_TOKEN, TEST_USER_ID = utl.enviroment_variables("Test")
    assert EXPECTED_OUTPUT_TEST_API_TOKEN == TEST_API_TOKEN and EXPECTED_OUTPUT_TEST_USER_ID == TEST_USER_ID


'''
DESCRIPTION:
This is an recrusiv test-methode where multiple test runs, which are defined in the Script_variables.
-------------------------------------------------------------------------------------------
FUNCTION WHICH IS TESTED:
information_extractor(content,extractor,parser)
'''
def test_information_extractor(content="<table><th>Unit Test</th></table>", extractor="th",
                               expected_result_string=[["th", "Unit Test"]], parser="html.parser"):
    soup = BeautifulSoup('', 'html.parser')
    result_from_methode = utl.information_extractor(content, extractor, parser)
    # New tag obeject from BeautifulSoup for testing
    expected_result_set = []
    for test in expected_result_string:
        new_tag = soup.new_tag(test[0])
        inner_content = BeautifulSoup(test[1], parser)
        for content in inner_content.contents:
            new_tag.append(content)
        # adds a new created tag element to the expected_result_set list
        expected_result_set.append(new_tag)
    expected_result_set = ResultSet(None, expected_result_set)
    if expected_result_set == result_from_methode:
        if TEST_RUNS_test_information_extractor:
            # If a run remains, take that run and remove it from the list of runs.
            run = TEST_RUNS_test_information_extractor.pop(0)
            # Execute the same method with the new run from all the test runs.
            test_information_extractor(run[0], run[1], run[2])
        # If this method executes up to here, the test is complete.
        assert expected_result_set == result_from_methode
    else:
        raise AssertionError(
            f"Expected result set {expected_result_set}, but received result set: {result_from_methode}.")
