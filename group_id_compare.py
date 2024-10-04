#!/usr/bin/python3

import argparse
import csv
import os
import pandas as pd

"""
    Description:
        Parses command-line arguments for base and compare files, file type, and property names.
    Args:
        None (arguments are provided via the command line).
    Returns:
        argparse.Namespace: Parsed arguments for base_file, compare_file, file type, and property names.
"""
def parse_arguments():
    parser = argparse.ArgumentParser(description="Compare groupings of identifiers between two files.")
    parser.add_argument('-base_file', required=True, help="Path to the base (golden) file")
    parser.add_argument('-compare_file', required=True, help="Path to the file to compare against")
    parser.add_argument('-type', required=True, choices=['csv', 'txt'], help="File type: 'csv' or 'txt'")
    parser.add_argument('-property_names', nargs='+', required=True, help="Property names: 2 for CSV, 1 for TXT")
    return parser.parse_args()

"""
    Description:
        Parses a CSV file and returns a dictionary mapping identifiers to group IDs.
    Args:
        file_path (str): Path to the CSV file.
        identifier_column (str): Column name for identifiers.
        group_column (str): Column name for group IDs.
    Returns:
        dict: A dictionary mapping identifiers to group IDs.
"""
def parse_csv_file(file_path, identifier_column, group_column):
    df = pd.read_csv(file_path)
    identifier_to_group_map = dict(zip(df[identifier_column], df[group_column]))
    return identifier_to_group_map

"""
    Description:
        Parses a TXT file with key-value pairs and returns a dictionary mapping identifiers to group IDs.
    Args:
        file_path (str): Path to the TXT file.
        group_property (str): The property name that defines the group ID in the file.
    Returns:
        dict: A dictionary mapping identifiers to group IDs.
"""
def parse_txt_file(file_path, group_property):
    identifier_to_group_map = {}
    current_identifier = None

    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith("Pattern"):
                current_identifier = line
            elif line.startswith(f"{group_property}:") and current_identifier:
                group_id = line.split(":")[1].strip()
                identifier_to_group_map[current_identifier] = group_id
    
    return identifier_to_group_map

"""
    Description:
        Compares two dictionaries of identifier-to-group mappings and checks if the groupings are consistent.
        Ignores the actual Group IDs and only compares the sets of identifiers.
    Args:
        base_group_map (dict): The group mappings from the base file.
        compare_group_map (dict): The group mappings from the compare file.
    Returns:
        tuple: A tuple containing a boolean result and a group ID mapping if the groupings match.
"""
def compare_group_mappings(base_group_map, compare_group_map):
    base_group_inverse = invert_group_mapping(base_group_map)
    compare_group_inverse = invert_group_mapping(compare_group_map)

    # Compare sets of identifiers, ignoring the group IDs
    base_groups = list(base_group_inverse.values())
    compare_groups = list(compare_group_inverse.values())

    # Sort the sets of identifiers to ensure order doesn't matter
    base_groups_sorted = sorted(base_groups, key=lambda x: sorted(x))
    compare_groups_sorted = sorted(compare_groups, key=lambda x: sorted(x))

    if base_groups_sorted == compare_groups_sorted:
        return True, create_group_id_mapping(base_group_map, compare_group_map)
    else:
        return False, {}

"""
    Description:
        Inverts a dictionary to group identifiers by their group IDs.
    Args:
        group_map (dict): A dictionary mapping identifiers to group IDs.
    Returns:
        dict: An inverted dictionary mapping group IDs to sets of identifiers.
"""
def invert_group_mapping(group_map):
    inverted_map = {}
    for identifier, group_id in group_map.items():
        if group_id not in inverted_map:
            inverted_map[group_id] = set()
        inverted_map[group_id].add(identifier)
    return inverted_map

"""
    Description:
        Creates a mapping of Group IDs between the base and comparison files.
    Args:
        base_group_map (dict): The group mappings from the base file.
        compare_group_map (dict): The group mappings from the compare file.
    Returns:
        dict: A dictionary mapping Group IDs from the base file to Group IDs in the compare file.
"""
def create_group_id_mapping(base_group_map, compare_group_map):
    group_id_mapping = {}
    base_group_inverse = invert_group_mapping(base_group_map)
    compare_group_inverse = invert_group_mapping(compare_group_map)

    for base_group_id, base_identifiers in base_group_inverse.items():
        for compare_group_id, compare_identifiers in compare_group_inverse.items():
            if base_identifiers == compare_identifiers:
                group_id_mapping[base_group_id] = compare_group_id

    return group_id_mapping

"""
    Description:
        The main function that handles argument parsing, file parsing, and comparison of groupings.
    Args:
        None
    Returns:
        None
"""
def main():
    args = parse_arguments()

    # Parse the base file and compare file
    if args.type == 'csv' and len(args.property_names) == 2:
        base_group_map = parse_csv_file(args.base_file, args.property_names[0], args.property_names[1])
        compare_group_map = parse_csv_file(args.compare_file, args.property_names[0], args.property_names[1])
    elif args.type == 'txt' and len(args.property_names) == 1:
        base_group_map = parse_txt_file(args.base_file, args.property_names[0])
        compare_group_map = parse_txt_file(args.compare_file, args.property_names[0])
    else:
        print("Invalid property names for the given file type.")
        exit(1)

    # Compare the groupings
    result, group_mapping = compare_group_mappings(base_group_map, compare_group_map)
    
    if result:
        print("Groupings match!")
        print(f"Group ID Mapping: {group_mapping}")
        exit(0)
    else:
        print("Groupings do not match!")
        exit(1)

if __name__ == "__main__":
    main()
