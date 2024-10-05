
# Group ID Compare Tool

## Description

The **Group ID Compare Tool** compares the grouping of elements between two files and checks if the same identifiers are grouped together, regardless of the specific group IDs assigned. This tool is useful when different tools or algorithms produce different group IDs, but the grouping pattern remains the same.

### Key Features
- Supports both **CSV** and **TXT** file formats.
- Compares identifiers to ensure they are grouped similarly in both files.
- Ignores specific group ID values and focuses on grouping consistency.
- Provides output with a mapping between group IDs in the two files when the grouping is consistent.
- Optionally provides analysis for debugging if the groupings do not match (Bonus feature).

## Requirements

The tool requires the following Python dependencies:
- `pandas`: For parsing CSV files.
- `argparse`: For handling command-line arguments.
- `os`: For checking file existence.

You can install the required dependencies using:

```bash
pip install pandas
```

## How to Use

This tool can be invoked from the command line with the following options:

### Command-Line Arguments

```bash
group_id_compare.py -base_file <file1> -compare_file <file2> -type <file_type> -property_names <list_of_property_names>
```

#### Arguments:
- `-base_file <file1>`: The path to the base file (golden data) containing the correct groupings.
- `-compare_file <file2>`: The path to the file to compare against the base file.
- `-type <file_type>`: The type of the input files, either `csv` or `txt`.
- `-property_names <list_of_property_names>`:
  - For CSV files: Provide **two** column names (one for the identifier and one for the group ID).
  - For TXT files: Provide **one** property name for the group ID (the identifier is detected automatically).

### Examples

#### Example 1: CSV Input

You have two CSV files that look like this:

`file1.csv`:
```
DefectID,cluster_ID
1,1
2,2
3,3
4,4
```

`file2.csv`:
```
DefectID,cluster_ID
1,5
2,6
3,7
4,8
```

Command to run:
```bash
python group_id_compare.py -base_file file1.csv -compare_file file2.csv -type csv -property_names 'DefectID' 'cluster_ID'
```

#### Example 2: TXT Input

You have two TXT files with the following structure:

`file1.txt`:
```
Pattern1
Class_id: 1
Pattern2
Class_id: 2
```

`file2.txt`:
```
Pattern1
Class_id: 5
Pattern2
Class_id: 6
```

Command to run:
```bash
python group_id_compare.py -base_file file1.txt -compare_file file2.txt -type txt -property_names 'Class_id'
```

### Output

- **Success**: If the groupings match, the script prints a mapping of the group IDs between the two files, like this:
  ```
  {'1': '5', '2': '6'}
  ```
  The script exits with status code `0`.

- **Failure**: If the groupings do not match, the script prints an error message and exits with status code `1`.


## Automated Testing

This project includes a comprehensive set of tests to ensure the correctness and reliability of the Group ID Comparison Script. 
The tests cover various functionalities such as CSV and TXT file loading, group comparison, error handling, and input validation.
To ensure the script works correctly, test it with:



### 1. **Dependencies**:
Before running the tests, ensure you have the following Python packages installed:

```bash
pip install pytest pytest-html pytest-mock
```

These dependencies include:
- pytest: To run the test cases.
- pytest-html: To generate an HTML report of the test results.
- pytest-mock: To mock certain behaviors during testing.

### 2. **Running the Tests**:
You can run the tests using pytest by following these steps:

1- Navigate to the directory where the test file is located.
2- Run the following command to execute all the test cases:

```bash
cd tests
pytest automated_test_cases.py
```
This will execute the entire test suite.

### 3. **Generating Test Reports**:
You can generate a detailed HTML report of the test results by using the following command:

```bash
pytest --html=../output/test_report.html --self-contained-html automated_test_cases.py
```
This will generate a report in ../output/test_report.html, which you can open in a browser to view the test results.

### 4. **Code Coverage**:
To check how much of the code is covered by the tests, you can run the following command:

```bash
coverage run --source=../src -m pytest automated_test_cases.py
```

To generate an HTML coverage report:

```bash
coverage html -d ../output/coverage
```

You can open the coverage report located in ../output/coverage/index.html to check which parts of the code are covered by the tests.


### 5. **Test Categories**:
The test cases are divided into the following categories:

- CSV and TXT Loading and Validation: Tests the loading of CSV and TXT files, ensuring proper error handling for missing columns, group properties, and invalid formats.
- Group Comparison and Error Handling: Tests the comparison of group IDs between base and comparison files.
- Input Validation: Tests to ensure that the script validates input files correctly based on the file type (CSV or TXT) and handles file type mismatches.
- Main Function Execution: Tests the main execution flow of the script, ensuring correct handling of input arguments and proper functionality.

By following these instructions, you can validate that the Group ID Comparison Script works as expected and ensure the reliability of its functionalities.

### 6. **Example Test Case:**:

**Input:**
- Base file (`file1.csv`):
  ```
  DefectID,cluster_ID
  A,5
  B,2
  C,3
  D,3
  G,2
  K,5
  L,4
  M,2
  ```

- Compare file (`file2.csv`):
  ```
  DefectID,cluster_ID
  C,7
  G,2
  K,36
  L,8
  M,2
  A,36
  D,7
  B,2
  ```

**Command:**
```bash
python group_id_compare.py -base_file file1.csv -compare_file file2.csv -type csv -property_names 'DefectID' 'cluster_ID'
```

**Expected Output:**
```
Groupings match!
{'5': '36', '2': '2', '3': '7', '4': '8'}
```
