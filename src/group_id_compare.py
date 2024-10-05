#!/usr/bin/python3

import argparse
import pandas as pd

"""
Description:
    Parses command-line arguments for base and compare files, file type, and property names.
Arguments:
    None (arguments are provided via the command line).
Returns:
    argparse.Namespace: Parsed arguments for base_file, compare_file, file type, and property_names.
"""
def get_cli_arguments():
    parser = argparse.ArgumentParser(description="Compare groupings of identifiers between two files.")
    parser.add_argument('-base_file', required=True, help="Path to the base (golden) file")
    parser.add_argument('-compare_file', required=True, help="Path to the file to compare against")
    parser.add_argument('-type', required=True, choices=['csv', 'txt'], help="File type: 'csv' or 'txt'")
    parser.add_argument('-property_names', nargs='+', required=True, help="Property names: 2 for CSV, 1 for TXT")
    return parser.parse_args()

"""
Description:
    Validates the input files and property names based on the type (CSV or TXT).
    Checks if the base and comparison files are of the same type.
    Ensures that the correct number of property names are provided for each file type.
    Verifies that the file extensions match the specified --type argument.

Arguments:
    args (argparse.Namespace): Parsed command-line arguments.

Returns:
    None. Raises an error and exits if validation fails.
"""
def validate_input_files(args):
    # Check if the file type is correct
    if args.type not in ['csv', 'txt']:
        print("Error: Unsupported file type. Please specify 'csv' or 'txt'.")
        exit(1)
    
    # Check for CSV file type and ensure exactly 2 property names
    if args.type == 'csv' and len(args.property_names) != 2:
        print("Error: CSV files should have exactly 2 property names (identifier and group property).")
        exit(1)
    
    # Check if file extensions match the file type
    if args.type == 'csv':
        if not args.base_file.endswith('.csv') or not args.compare_file.endswith('.csv'):
            print("Error: The file type is specified as CSV, but one or both input files do not have a .csv extension.")
            exit(1)
    elif args.type == 'txt':
        if not args.base_file.endswith('.txt') or not args.compare_file.endswith('.txt'):
            print("Error: The file type is specified as TXT, but one or both input files do not have a .txt extension.")
            exit(1)

    # Check for empty property names
    if not args.property_names:
        print("Error: Property names are missing.")
        exit(1)

    # Other validations...


"""
Description:
    Loads and validates the CSV file, ensuring the required identifier and group columns exist.
    Creates a dictionary mapping identifiers to their corresponding group IDs.
Arguments:
    file_path (str): Path to the CSV file.
    identifier_column (str): Column name for identifiers (e.g., Identifier_ID).
    group_column (str): Column name for group IDs (e.g., Group_ID).
Returns:
    dict: A dictionary mapping identifiers to group IDs.
Raises:
    ValueError: If the file does not contain the required columns or there is an issue reading the file.
""" 
def load_and_validate_csv(file_path, identifier_column, group_column):
    try:
        # Load the CSV file into a DataFrame
        df = pd.read_csv(file_path)
        
        # Check if the DataFrame is empty
        if df.empty:
            raise ValueError(f"The CSV file '{file_path}' is empty.")
        
        # Check if the required columns are present
        if identifier_column not in df.columns or group_column not in df.columns:
            raise ValueError(f"CSV file must contain '{identifier_column}' and '{group_column}' columns.")

        # Check for missing values
        if df[identifier_column].isnull().any() or df[group_column].isnull().any():
            raise ValueError(f"CSV file '{file_path}' contains missing values in required columns.")
        
        # Create a dictionary mapping identifiers to group IDs
        return dict(zip(df[identifier_column], df[group_column]))

    except Exception as e:
        raise ValueError(f"Error loading or validating CSV file '{file_path}': {str(e)}")

"""
Description:
    Loads and validates the TXT file, ensuring that it contains the user-specified identifier and group properties.
    Creates a dictionary mapping identifiers to their corresponding group IDs.
Arguments:
    file_path (str): Path to the TXT file.
    identifier_property (str): The property name that defines the identifier (e.g., Identifier_ID).
    group_property (str): The property name that defines the group ID in the file (e.g., Class_id).
Returns:
    dict: A dictionary mapping identifiers to group IDs.
Raises:
    ValueError: If the file does not contain valid identifiers or the specified group property.
"""
def load_and_validate_txt(file_path, group_property):
    identifier_group_mapping = {}
    current_identifier = None
    is_group_property_found = False

    try:
        with open(file_path, 'r') as f:
            for line in f:
                line = line.strip()

                # Check if it's an identifier line (no colon)
                if ":" not in line and line != "":
                    current_identifier = line

                # Check for the group property
                elif line.startswith(f"{group_property}:") and current_identifier:
                    group_id = line.split(":")[1].strip()  # Extract the group ID
                    identifier_group_mapping[current_identifier] = group_id
                    is_group_property_found = True

                # If group property is found without an identifier
                if not current_identifier:
                    raise ValueError(f"Identifier missing before '{group_property}' in the file.")

        if not is_group_property_found:
            raise ValueError(f"File '{file_path}' does not contain the specified group property: '{group_property}'.")

    except Exception as e:
        raise ValueError(f"Error validating and parsing TXT file '{file_path}': {str(e)}")

    return identifier_group_mapping

"""
Description:
    Compares the groupings of identifiers between the base file and the comparison file.
    Ignores the actual Group IDs and only checks whether the sets of identifiers match between the two files.
Arguments:
    base_identifier_group_map (dict): The group mappings from the base file (identifier -> group ID).
    compare_identifier_group_map (dict): The group mappings from the compare file (identifier -> group ID).
Returns:
        tuple: (bool, dict or None) 
            - True and the Group ID mapping if groupings match.
            - False and None if groupings do not match.
"""
def compare_identifier_groups(base_identifier_group_map, compare_identifier_group_map):
    grouped_identifiers_base = group_identifiers_by_group_id(base_identifier_group_map)
    grouped_identifiers_compare = group_identifiers_by_group_id(compare_identifier_group_map)

    sorted_grouped_identifiers_base = sorted(grouped_identifiers_base.values(), key=lambda x: sorted(x))
    sorted_grouped_identifiers_compare = sorted(grouped_identifiers_compare.values(), key=lambda x: sorted(x))
    
    if sorted_grouped_identifiers_base == sorted_grouped_identifiers_compare:
        # Return True and the Group ID mapping
        group_id_mapping = create_group_id_mapping(grouped_identifiers_base, grouped_identifiers_compare)
        return True, group_id_mapping
    else:
        return False, None

"""
Description:
    Creates a mapping of Group IDs between the base file and the comparison file.
    The function compares the sets of identifiers in the base file and the comparison file,
    and maps the corresponding Group IDs if the identifier sets match.

Arguments:
    base_group (dict): A dictionary mapping Group IDs to sets of identifiers from the base file (Group ID -> {Set of Identifiers}).
    compare_group (dict): A dictionary mapping Group IDs to sets of identifiers from the comparison file (Group ID -> {Set of Identifiers}).

Returns:
    dict: A dictionary mapping Group IDs from the base file to Group IDs from the comparison file (Base Group ID -> Comparison Group ID).
"""
def create_group_id_mapping(base_group, compare_group):
    group_mapping = {}
    for base_id, base_identifiers in base_group.items():
        for compare_id, compare_identifiers in compare_group.items():
            if base_identifiers == compare_identifiers:
                group_mapping[base_id] = compare_id
    return group_mapping

"""
Description:
    Inverts a dictionary to group identifiers by their group IDs, returning a mapping of group IDs to sets of identifiers.
Arguments:
    group_map (dict): A dictionary mapping identifiers to group IDs (identifier -> group ID).
Returns:
    dict: A dictionary mapping group IDs to sets of identifiers (Group ID -> {Set of identifiers}).
"""
def group_identifiers_by_group_id(group_map):
    inverted_map = {}
    for identifier, group_id in group_map.items():
        if group_id not in inverted_map:
            inverted_map[group_id] = set()
        inverted_map[group_id].add(identifier)
    return inverted_map

"""
Description:
    Main function to handle command-line argument parsing and the overall comparison process between base and comparison files.
    Loads the appropriate files (CSV or TXT), compares the groupings, and prints the result (success or failure).
Arguments:
    None (arguments are provided via the command line).
Returns:
    None.
"""        
def main():
    args = get_cli_arguments()

    # Call the validation function to validate the inpute files before proceeding
    validate_input_files(args)

    # Handling CSV files
    if args.type == 'csv':
        base_identifier_to_group_map = load_and_validate_csv(args.base_file, args.property_names[0], args.property_names[1])
        compare_identifier_to_group_map = load_and_validate_csv(args.compare_file, args.property_names[0], args.property_names[1])

    # Handling TXT files
    elif args.type == 'txt':
        base_identifier_to_group_map = load_and_validate_txt(args.base_file, args.property_names[0])
        compare_identifier_to_group_map = load_and_validate_txt(args.compare_file, args.property_names[0])

    # Compare groupings and get the result and mappings
    result, group_id_mapping = compare_identifier_groups(base_identifier_to_group_map, compare_identifier_to_group_map)

    if result:
        print("Success: Groupings match!")
        print(f"Group ID Mapping: {group_id_mapping}")
        exit(0)
    else:
        print("Failure: Groupings do not match!")
        exit(1)


if __name__ == "__main__":
    main()
