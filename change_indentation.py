#
# Usage:
#
# python change_indentation.py <folder_location> <number_of_spaces> <file_extension>
# e.g. python change_indentation.py . 4 py  (changes indentation in all files ending with py in current folder by 4 spaces)
#
import argparse
import os
import re

parser = argparse.ArgumentParser(description='Replace tabs/2spaces with tab.')
parser.add_argument('root_directory', type=str, default='.', nargs='?',
                   help='directory to run the script in')
parser.add_argument('spaces', type=int, default=2, nargs='?',
                   help='number of spaces for one tab')
parser.add_argument('file_type', type=str, default=".*", nargs='?',
                   help='file type')

args = parser.parse_args()
file_type = re.compile(".*/*\.{}$".format(args.file_type))
replacement_spaces = ' ' * args.spaces

print('Starting indentation change. \
directory {0}, spaces {1}, file mask {2}'.format(args.root_directory, args.spaces, args.file_type))

found_files = []
for path, subdirs, files in os.walk(args.root_directory):
    for name in files:
        found_files.append(os.path.join(path, name))

matched_files = [name for name in found_files if file_type.match(name)]

for file_path in matched_files:
    file_contents = list()
    already_indented = False
    first_indented_line = None
    current_indentation = None
    with open(file_path) as f:
        for line in f:
            if (line.startswith(" ") or line.startswith("\t")) and first_indented_line is None:
                first_indented_line = line
                current_indentation = line[:(len(line) - len(line.lstrip()))]
                if current_indentation == replacement_spaces:
                    already_indented = True

            if not already_indented and current_indentation:
                if len(line.lstrip()) > 0 and len(line) - len(line.lstrip()) > 0:
                    current_indentation_number = line[:(len(line) - len(line.lstrip()))].count(current_indentation)
                    line = (replacement_spaces * current_indentation_number) + line.lstrip()
            file_contents.append(line)

    print('Changing indentation in {0}'.format(file_path))
    with open(file_path, "w") as f:
        for line in file_contents:
            f.write(line)

print('Done')
