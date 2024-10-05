#!/usr/bin/python3

import pytest
import os
import sys
sys.path.append('../src')
from group_id_compare import (
    main, validate_input_files, load_and_validate_csv, load_and_validate_txt,
    compare_identifier_groups, group_identifiers_by_group_id, create_group_id_mapping
)

# Define the test data directory and file paths
TEST_DATA_DIR = "../test_data"
BASE_CSV = os.path.join(TEST_DATA_DIR, 'base_file.csv')
COMPARE_CSV = os.path.join(TEST_DATA_DIR, 'compare_file.csv')
COMPARE_DIFF_CSV = os.path.join(TEST_DATA_DIR, 'compare_diff_file.csv')
BASE_TXT = os.path.join(TEST_DATA_DIR, 'base_file.txt')
COMPARE_TXT = os.path.join(TEST_DATA_DIR, 'compare_file.txt')


# Test Case 1: Validate CSV loading with correct data
def test_load_and_validate_csv():
    identifier_group_map = load_and_validate_csv(BASE_CSV, 'IdentifierID', 'GroupID')
    assert identifier_group_map == {
        "A": 5,
        "B": 2,
        "C": 3,
        "D": 3,
        "G": 2,
        "K": 5,
        "L": 4,
        "M": 2
    }

# Test Case 2: Validate TXT loading with correct data
def test_load_and_validate_txt():
    identifier_group_map = load_and_validate_txt(BASE_TXT, 'Class_id')
    assert identifier_group_map == {
        "Pattern1": '1',
        "Pattern2": '2',
        "Pattern3": '1',
        "Pattern4": '3',
        "Pattern5": '3',
        "Pattern6": '2'
    }

# Test Case 3: Validate error handling for CSV with missing column
def test_load_and_validate_csv_missing_column():
    invalid_csv = os.path.join(TEST_DATA_DIR, 'invalid_file.csv')
    with pytest.raises(ValueError):
        load_and_validate_csv(invalid_csv, 'IdentifierID', 'GroupID')

# Test Case 4: Validate error handling for TXT with missing group property
def test_load_and_validate_txt_missing_property():
    invalid_txt = os.path.join(TEST_DATA_DIR, 'invalid_file.txt')
    with pytest.raises(ValueError):
        load_and_validate_txt(invalid_txt, 'Class_id')

# Test Case 5: Validate correct group comparison between base CSV and comparison TXT
def test_compare_identifier_groups():
    base_group_map = load_and_validate_txt(BASE_TXT, 'Class_id')
    compare_group_map = load_and_validate_txt(COMPARE_TXT, 'Class_id')
    
    result, group_id_mapping = compare_identifier_groups(base_group_map, compare_group_map)
    assert result is True
    assert group_id_mapping == {"1": "10", "2": "36", "3": "7"}

# Test Case 6: Validate group comparison failure for mismatched data
def test_compare_identifier_groups_mismatch():
    base_group_map = load_and_validate_csv(BASE_CSV, 'IdentifierID', 'GroupID')
    compare_group_map = load_and_validate_txt(COMPARE_TXT, 'Class_id')
    
    result, group_id_mapping = compare_identifier_groups(base_group_map, compare_group_map)
    assert result is False
    assert group_id_mapping is None

# Test Case 7: Validate input files when CSV type is provided with valid arguments
def test_validate_input_files_csv(mocker):
    mock_args = mocker.Mock()
    mock_args.type = 'csv'
    mock_args.base_file = BASE_CSV
    mock_args.compare_file = COMPARE_CSV
    mock_args.property_names = ['IdentifierID', 'GroupID']
    validate_input_files(mock_args)

# Test Case 8: Validate input files when TXT type is provided with valid arguments
def test_validate_input_files_txt(mocker):
    mock_args = mocker.Mock()
    mock_args.type = 'txt'
    mock_args.base_file = BASE_TXT
    mock_args.compare_file = COMPARE_TXT
    mock_args.property_names = ['Class_id']
    validate_input_files(mock_args)

# Test Case 9: Validate error handling for mismatched file types (CSV and TXT)
def test_validate_input_files_mismatch_type(mocker):
    mock_args = mocker.Mock()
    mock_args.type = 'csv'
    mock_args.base_file = BASE_TXT
    mock_args.compare_file = COMPARE_CSV
    mock_args.property_names = ['IdentifierID', 'GroupID']
    
    with pytest.raises(SystemExit):
        validate_input_files(mock_args)

# Test Case 10: Test grouping of identifiers by group ID
def test_group_identifiers_by_group_id():
    identifier_group_map = {
        "Pattern1": "1",
        "Pattern2": "2",
        "Pattern3": "1"
    }
    grouped = group_identifiers_by_group_id(identifier_group_map)
    assert grouped == {
        "1": {"Pattern1", "Pattern3"},
        "2": {"Pattern2"}
    }

# Test Case 11: Test creating group ID mapping between base and comparison files
def test_create_group_id_mapping():
    base_group = {
        "1": {"Pattern1", "Pattern3"},
        "2": {"Pattern2"}
    }
    compare_group = {
        "1": {"Pattern1", "Pattern3"},
        "2": {"Pattern2"}
    }
    mapping = create_group_id_mapping(base_group, compare_group)
    assert mapping == {"1": "1", "2": "2"}

# Test Case 12: Validate empty CSV file handling
def test_load_and_validate_empty_csv():
    empty_csv = os.path.join(TEST_DATA_DIR, 'empty_file.csv')
    with pytest.raises(ValueError):
        load_and_validate_csv(empty_csv, 'IdentifierID', 'GroupID')

# Test Case 13: Validate empty TXT file handling
def test_load_and_validate_empty_txt():
    empty_txt = os.path.join(TEST_DATA_DIR, 'empty_file.txt')
    with pytest.raises(ValueError):
        load_and_validate_txt(empty_txt, 'Class_id')

# Test Case 14: Validate incorrect group property format in TXT
def test_load_and_validate_txt_invalid_format():
    invalid_format_txt = os.path.join(TEST_DATA_DIR, 'invalid_format_file.txt')
    with pytest.raises(ValueError):
        load_and_validate_txt(invalid_format_txt, 'Class_id')

# Test Case 15: Validate mismatched group ID formats (string vs integer)
def test_compare_identifier_groups_mismatched_group_id_format():
    base_group_map = {
        "Pattern1": "1",
        "Pattern2": "2",
        "Pattern3": "1"
    }
    compare_group_map = {
        "Pattern1": "1",
        "Pattern2": "2",
        "Pattern3": "1"
    }
    result, group_id_mapping = compare_identifier_groups(base_group_map, compare_group_map)
    assert result is True
    assert group_id_mapping == {"1": "1", "2": "2"}

# Test Case 16: Validate error handling for incorrect group property name in TXT
def test_load_and_validate_txt_incorrect_group_property():
    invalid_group_property_txt = os.path.join(TEST_DATA_DIR, 'incorrect_group_property.txt')
    with pytest.raises(ValueError):
        load_and_validate_txt(invalid_group_property_txt, 'WrongProperty')

# Test Case 17: CSV with extra, unexpected columns
def test_load_and_validate_csv_extra_columns():
    extra_column_csv = os.path.join(TEST_DATA_DIR, 'extra_column_file.csv')
    identifier_group_map = load_and_validate_csv(extra_column_csv, 'IdentifierID', 'GroupID')
    assert identifier_group_map == {
        "A": 1,
        "B": 2,
        "C": 1
    }

# Test Case 18: Malformed CSV file (missing values)
def test_load_and_validate_csv_malformed():
    malformed_csv = os.path.join(TEST_DATA_DIR, 'malformed_file.csv')
    with pytest.raises(ValueError):
        load_and_validate_csv(malformed_csv, 'IdentifierID', 'GroupID')

# Test Case 19: TXT with missing identifier
def test_load_and_validate_txt_missing_identifier():
    missing_identifier_txt = os.path.join(TEST_DATA_DIR, 'missing_identifier_file.txt')
    with pytest.raises(ValueError):
        load_and_validate_txt(missing_identifier_txt, 'Class_id')

# Test Case 20: TXT with only one identifier
def test_load_and_validate_txt_single_identifier():
    single_identifier_txt = os.path.join(TEST_DATA_DIR, 'single_identifier_file.txt')
    identifier_group_map = load_and_validate_txt(single_identifier_txt, 'Class_id')
    assert identifier_group_map == {
        "Pattern1": "1"
    }

# Test Case 21: Invalid argument for file type (non-txt or csv)
def test_validate_input_files_invalid_type(mocker):
    mock_args = mocker.Mock()
    mock_args.type = 'invalid_type'
    mock_args.base_file = BASE_CSV
    mock_args.compare_file = COMPARE_CSV
    mock_args.property_names = ['IdentifierID', 'GroupID']

    with pytest.raises(SystemExit):
        validate_input_files(mock_args)

# Test Case 22: Main function successful execution for CSV
def test_main_csv_pos_execution(mocker):
    mocker.patch('sys.argv', ['group_id_compare.py', '-type', 'csv', '-base_file', BASE_CSV, '-compare_file', COMPARE_CSV, '-property_names', 'IdentifierID', 'GroupID'])
    mocker.patch('group_id_compare.load_and_validate_csv', return_value={"A": 1, "B": 2, "C": 1})
    mocker.patch('group_id_compare.compare_identifier_groups', return_value=(True, {"1": "1", "2": "2"}))

    with pytest.raises(SystemExit) as e:
        main()  # Run the main function with mocked arguments and functions
    assert e.value.code == 0  # Ensure SystemExit code is 0 for success

# Test Case 23: Main function failure execution for CSV
def test_main_csv_neg_execution(mocker):
    mocker.patch('sys.argv', ['group_id_compare.py', '-type', 'csv', '-base_file', BASE_CSV, '-compare_file', COMPARE_DIFF_CSV, '-property_names', 'IdentifierID', 'GroupID'])

    with pytest.raises(SystemExit) as e:
        main()
    assert e.value.code == 1  # Ensure SystemExit code is 1 for failure

# Test Case 24: Main function successful execution for TXT
def test_main_txt_execution(mocker):
    mocker.patch('sys.argv', ['group_id_compare.py', '-type', 'txt', '-base_file', BASE_TXT, '-compare_file', COMPARE_TXT, '-property_names', 'Class_id'])
    mocker.patch('group_id_compare.load_and_validate_txt', return_value={"Pattern1": '1', "Pattern2": '2', "Pattern3": '1'})
    mocker.patch('group_id_compare.compare_identifier_groups', return_value=(True, {"1": "10", "2": "36", "3": "7"}))
    
    with pytest.raises(SystemExit) as e:
        main()  # Run the main function with mocked arguments and functions
    assert e.value.code == 0  # Ensure SystemExit code is 0 for success

# Test Case 25: Main function invalid file type
def test_main_invalid_type(mocker):
    mocker.patch('sys.argv', ['group_id_compare.py', '--type', 'invalid', '--base_file', BASE_CSV, '--compare_file', COMPARE_CSV, '--property_names', 'IdentifierID', 'GroupID'])
    
    with pytest.raises(SystemExit):  # Expecting SystemExit for invalid type
        main()

# Test Case 26: Validate input files with invalid file extension for CSV
def test_validate_input_files_invalid_file_extension(mocker):
    mock_args = mocker.Mock()
    mock_args.type = 'csv'
    mock_args.base_file = 'base_file.txt'  # Mismatched file extension for csv type
    mock_args.compare_file = 'compare_file.csv'
    mock_args.property_names = ['IdentifierID', 'GroupID']
    
    with pytest.raises(SystemExit):  # Expecting SystemExit due to file extension mismatch
        validate_input_files(mock_args)

# Test Case 27: Validate input files with missing property name
def test_validate_input_files_missing_property_name(mocker):
    mock_args = mocker.Mock()
    mock_args.type = 'txt'
    mock_args.base_file = BASE_TXT
    mock_args.compare_file = COMPARE_TXT
    mock_args.property_names = []  # Missing property names
    
    with pytest.raises(SystemExit):  # Expecting SystemExit due to missing property name
        validate_input_files(mock_args)

# Test Case 28: Validate input files with invalid type
def test_validate_input_files_invalid_type(mocker):
    mock_args = mocker.Mock()
    mock_args.type = 'invalid_type'  # Invalid file type
    mock_args.base_file = BASE_CSV
    mock_args.compare_file = COMPARE_CSV
    mock_args.property_names = ['IdentifierID', 'GroupID']
    
    with pytest.raises(SystemExit):  # Expecting SystemExit due to invalid file type
        validate_input_files(mock_args)

# Test Case 29: Validate input files with TXT base and CSV compare files
def test_validate_input_files_txt_base_csv_compare(mocker):
    mock_args = mocker.Mock()
    mock_args.type = 'txt'
    mock_args.base_file = 'base_file.txt'
    mock_args.compare_file = 'compare_file.csv'
    mock_args.property_names = ['Class_id']

    mock_print = mocker.patch('builtins.print')  # Correctly patch the print function
    with pytest.raises(SystemExit) as e:
        validate_input_files(mock_args)

    # Check that the correct error message was printed
    mock_print.assert_called_with("Error: The file type is specified as TXT, but one or both input files do not have a .txt extension.")
    assert e.value.code == 1  # Ensure it exits with code 1

# Test Case 30: Validate input files with invalid extension for TXT
def test_validate_input_files_invalid_extension_for_txt(mocker):
    mock_args = mocker.Mock()
    mock_args.type = 'txt'
    mock_args.base_file = 'base_file.csv'  # Invalid extension
    mock_args.compare_file = 'compare_file.txt'
    mock_args.property_names = ['Class_id']

    mock_print = mocker.patch('builtins.print')
    with pytest.raises(SystemExit) as e:
        validate_input_files(mock_args)

    mock_print.assert_called_with("Error: The file type is specified as TXT, but one or both input files do not have a .txt extension.")
    assert e.value.code == 1

# Test Case 31: Validate input files for CSV with only one property name
def test_validate_input_files_csv_with_one_property_name(mocker):
    mock_args = mocker.Mock()
    mock_args.type = 'csv'
    mock_args.base_file = 'base_file.csv'
    mock_args.compare_file = 'compare_file.csv'
    mock_args.property_names = ['IdentifierID']  # Only one property name

    mock_print = mocker.patch('builtins.print')
    with pytest.raises(SystemExit) as e:
        validate_input_files(mock_args)

    mock_print.assert_called_with("Error: CSV files should have exactly 2 property names (identifier and group property).")
    assert e.value.code == 1
