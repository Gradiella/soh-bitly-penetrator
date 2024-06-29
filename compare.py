import argparse

def read_file(filepath):
    """Read a file and return a set of its lines."""
    with open(filepath, 'r') as file:
        return set(line.strip() for line in file)

def compare_files(file1, file2):
    """Compare two sets of lines from two files."""
    set1 = read_file(file1)
    set2 = read_file(file2)

    matched = set1 & set2
    only_in_file1 = set1 - set2
    only_in_file2 = set2 - set1

    return len(set1), len(set2), len(matched), only_in_file1, only_in_file2

def main():
    parser = argparse.ArgumentParser(description="Compare two text files line by line.")
    parser.add_argument("file1", help="Path to the first text file.")
    parser.add_argument("file2", help="Path to the second text file.")
    args = parser.parse_args()

    file1_entries, file2_entries, matched_entries, only_in_file1, only_in_file2 = compare_files(args.file1, args.file2)

    print(f"{args.file1} has {file1_entries} entries")
    print(f"{args.file2} has {file2_entries} entries")
    print(f"{matched_entries} entries matched")
    print(f"{len(only_in_file1)} entries exist in {args.file1} but not in {args.file2}")
    print(f"{len(only_in_file2)} entries exist in {args.file2} but not in {args.file1}")

if __name__ == "__main__":
    main()