from src.utils import utils as utl

# Script_variables:
TEST_RUNS_test_create_abbreviation = [["Second_Test", "ST", ["AB", "TI"]]]


# utl.enviroment_variables("Produktname als string")
# utl.create_abbreviation("Name für Kürzel", listeExistierenderKürzel = [])

def test_create_abbreviation(string = "Initial Test", abbreviation = "IT", existing_abbreviations = ["AB", "TI"]):
    # Check if abbreviation already exist in list existing_abbreviations. If not included contiue with the test.
    # If it already exist, then test fails.
    if abbreviation not in existing_abbreviations:
        # Get the abbreviation from the methode.
        abbreviation_from_methode = utl.create_abbreviation(string,existing_abbreviations)
        # Check if the expected abbrevation is the same as the returned abbrevation from the methode.
        # If true (they are the same then continue with the test. If false then fail the test.
        if abbreviation == abbreviation_from_methode:
            # Check if there is still an run left in the Script_variable.
            if TEST_RUNS_test_create_abbreviation:
                # If run left, then take this run and delete ist from the list of runs.
                # Does this until there is no run left.
                run = TEST_RUNS_test_create_abbreviation.pop(0)
                # Executes the same methode with the new run from all Testruns.
                test_create_abbreviation(run[0],run[1],run[2])
            # If this methode executes until here, then the test is done.
            assert True == True
        else:
            assert False == True
    else:
        assert False == True


if __name__ == "__main__":
    test_create_abbreviation()
    print("Test")

