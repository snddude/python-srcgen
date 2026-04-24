from os import listdir
from os.path import join, splitext, isdir, isfile
from sys import argv
import argparse

PATH_SOURCELIST_FILE = "sourcelist.cmake"

path_project_directory = ""
path_sourcelist_directory = ""
path_exclude_directories = []
source_file_extensions = []

sources = []


def parse_folder(folder_path):
    for entry in listdir(folder_path):
        sub_path = join(folder_path, entry)

        if sub_path in path_exclude_directories:
            continue

        if isdir(sub_path):
            parse_folder(sub_path)
            continue

        if not isfile(sub_path):
            continue

        if splitext(sub_path)[1] in source_file_extensions:
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
    "-e",
    "--extensions",
    help="source file extensions to look for",
    required=True,
    nargs="+")
parser.add_argument(
    "-x",
    "--exclude",
    help="paths to folders to exclude from search",
    required=False,
    nargs="+")


args = parser.parse_args()

path_project_directory = args.input
source_file_extensions = args.extensions

path_sourcelist_directory = args.output if args.output else path_project_directory
path_exclude_directories = args.exclude if args.exclude else "None"


print(f"\n{argv[0]}:")
print(f"  input directory: {path_project_directory}")
print(f"  output directory: {path_sourcelist_directory}")
print(f"  extensions: {source_file_extensions}")
print(f"  exclusions: {path_exclude_directories}\n")

parse_folder(path_project_directory)
print()


with open(join(path_sourcelist_directory, PATH_SOURCELIST_FILE), "w") as file:
    file.write("set(SOURCES ${SOURCES}\n")

    for source in sources:
        file.write(f"\t{source}\n")

    file.write(")")
