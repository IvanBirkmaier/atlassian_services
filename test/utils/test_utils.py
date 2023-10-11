from src.utils import utils as utl

# Script_variables:
TEST_RUNS_test_create_abbreviation = [["Second_Test", "SE", ["AB", "TI"]], ["thridTest", "THR", ["AB", "TH"]],
                                      ["A", "AA", ["AB", "TI"]], ["fifth test", "FTF", ["AB", "FT"]],
                                      ["$4 444", "AA", ["AB", "FT"]],  ["$4 444", "AC", ["AB", "FT", "AA"]],  ["$4 444", "AD", ["AB", "FT","AA","AC"]] ]


'''
This is an recrusiv test-methode where multiple test runs, which are defined in the Script_variables. It tests the methode of. 
Teste methode: create_abbreviation
File: src.utils.utils
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
Teste methode: enviroment_variables
File: src.utils.utils
'''
def test_enviroment_variables():
    EXPECTED_OUTPUT_TEST_API_TOKEN = "12345Token"
    EXPECTED_OUTPUT_TEST_USER_ID = "max.mustermann@test.com"
    TEST_API_TOKEN, TEST_USER_ID = utl.enviroment_variables("Test")
    if EXPECTED_OUTPUT_TEST_API_TOKEN == TEST_API_TOKEN & EXPECTED_OUTPUT_TEST_USER_ID == TEST_USER_ID:
        assert True == True
    else:
        raise AssertionError(f"The received output from utl.enviroment_variables() isnot the same as expected")
