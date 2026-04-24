import argparse
from sys import argv
from os import listdir
from os.path import join, splitext, isdir, isfile, abspath

PATH_SOURCELIST_FILE = "sourcelist.cmake"


def search_folder(input_folder, excluded_folders, file_extensions):
    sources = []

    for entry in listdir(input_folder):
        sub_path = join(input_folder, entry)

        if sub_path in excluded_folders:
            continue

        if isdir(sub_path):
            sources += search_folder(
                sub_path, excluded_folders, file_extensions)
            continue

        if not isfile(sub_path):
            continue

        if splitext(sub_path)[1] in file_extensions:
            sources.append(sub_path)
            print(f"  discovered: {sub_path}")

    return sources


# Command line argument handling

parser = argparse.ArgumentParser(
    description="A Python script for generating sourcelist.cmake files")

parser.add_argument(
    "-i",
    "--input",
    help="path to folder in which to search for source files",
    required=True)
parser.add_argument(
    "-o",
    "--output",
    help=f"path to folder in which to put the {PATH_SOURCELIST_FILE} file. If not specified, the file will be put into --input",
    required=False)
parser.add_argument(
    "-x",
    "--exclude",
    help="paths to folders to exclude from search",
    required=False,
    nargs="+")
parser.add_argument(
    "-e",
    "--extensions",
    help="source file extensions to look for",
    required=True,
    nargs="+")
parser.add_argument(
    "-t",
    "--target",
    help="cmake target name",
    required=False)

args = parser.parse_args()


# Print parameters

print(f"\nRunning {argv[0]}...")
if args.target:
    print(f"  target: {args.target}")

print(f"  input directory: {args.input}")

output = args.output if args.output else args.input
print(f"  output directory: {args.output}")

print("  extensions:", str(args.extensions).replace("'", "")[1:-1])

exclusions = []
if args.exclude:
    exclusions = args.exclude
    print(f"  exclusions: {exclusions}")

print()


# Search input folder and write output to file (if any source files were found)

sources = search_folder(args.input, exclusions, args.extensions)

if len(sources) > 0:
    filepath = join(args.output, PATH_SOURCELIST_FILE)

    with open(filepath, "w") as file:
        file.write("set(SOURCES ${SOURCES}\n")

        for source in sources:
            file.write(f"\t{source}\n")

        file.write(")\n")

    print(f"Found source files written to: {abspath(filepath)}")
else:
    print("No source files found")
