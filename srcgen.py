from os import listdir
from os.path import join, splitext, isdir, isfile
from sys import argv
import argparse

PATH_SOURCELIST_FILE = "sourcelist.cmake"

path_input_folder = ""
path_output_folder = ""
path_excluded_folders = []
file_extensions = []

sources = []


def parse_folder(folder_path):
    for entry in listdir(folder_path):
        sub_path = join(folder_path, entry)

        if sub_path in path_excluded_folders:
            continue

        if isdir(sub_path):
            parse_folder(sub_path)
            continue

        if not isfile(sub_path):
            continue

        if splitext(sub_path)[1] in file_extensions:
            sources.append(sub_path)
            print(f"  discovered: {sub_path}")


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
    help=f"path to folder in which to put the {PATH_SOURCELIST_FILE} file",
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

print(f"Running {argv[0]}...")

args = parser.parse_args()

if args.target:
    print(f"  target: {args.target}")

path_input_folder = args.input
print(f"  input directory: {path_input_folder}")

path_output_folder = args.output if args.output else path_input_folder
print(f"  output directory: {path_output_folder}")

file_extensions = args.extensions
print(f"  extensions: {file_extensions}")

path_excluded_folders = args.exclude if args.exclude else "None"
print(f"  exclusions: {path_excluded_folders}\n")

parse_folder(path_input_folder)


with open(join(path_output_folder, PATH_SOURCELIST_FILE), "w") as file:
    file.write("set(SOURCES ${SOURCES}\n")

    for source in sources:
        file.write(f"\t{source}\n")

    file.write(")")
