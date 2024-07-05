import os
import sys
import argparse

parser = argparse.ArgumentParser(description='filter out smithRNAs that has sharp peaks')
parser.add_argument('--delimiter', type=str, default='//', help='select delimiter value to split files, "//" is (default)')
parser.add_argument('--input_file', type=str, required=True, help='file to be split, is mandatory to have one')
args = parser.parse_args()

#need the name for defining the following definition
input_file = args.input_file

def split_file(input_file, delimiter=args.delimiter, output_dir=str(input_file.split(".")[0]) + ".output_files"):
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    with open(input_file, 'r') as file:
        file_content = file.read()

    # Split the content based on the delimiter
    sections = file_content.split(delimiter)

    # Write each section to a new file
    for index, section in enumerate(sections):
        output_file_path = os.path.join(output_dir, f"section_{index + 1}.txt")
        with open(output_file_path, 'w') as output_file:
            output_file.write(section.strip() + "\n")

    print(f"File split into {len(sections)} sections and saved in {output_dir}")

# Example usage
split_file(input_file)
