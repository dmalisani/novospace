import pdb
import sys
import argparse
import re
import os
import io

parser=argparse.ArgumentParser()
DUMP_MEMORY_FILENAME = "memdump0.mem"

parser.add_argument('-i', help='Input file', required=True)
parser.add_argument('-o', help='Outputfile', required=True)

args=parser.parse_args()
input_file = args.i
output_file = args.o

if not os.path.isfile(input_file):
    print("Input file doesn't exist")
    sys.exit(os.EX_OSFILE)

DETECT_REGEX = "reg \[(.*)\] (\S*) \[(.*)\];\n  initial begin\n((    \S*\[\S*\] = \S*;\n)*)  end\n"

with open(input_file, "r") as f:
    input_content = f.read()

memory_values = re.search(DETECT_REGEX, input_content)
memory_splits = [a.split("=")[1].strip().split("'h")[1][:-1] for a in memory_values.group(4).split("\n")[:-1]]

new_string = f"reg [{memory_values.group(1)}] {memory_values.group(2)} [{memory_values.group(3)}];\n"
new_string += f'$readmemh("{DUMP_MEMORY_FILENAME}", {memory_values.group(2)});\n'
output_content = input_content.replace(input_content[memory_values.start(0):memory_values.end(0)], new_string)

with open(DUMP_MEMORY_FILENAME, "w") as f:
    f.write('\n'.join(memory_splits) + '\n')

with open(output_file, "w") as f:
    f.write(output_content)

