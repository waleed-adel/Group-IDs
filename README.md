
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


## Testing

To ensure the script works correctly, test it with:
- Different input formats (`CSV` and `TXT`).
- Various grouping combinations.
- Large datasets to assess performance.

### Example Test Case:

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
