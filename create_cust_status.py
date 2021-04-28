import re
import sys
import os

with open ("OUTPUTS\Status.asc", "r") as myfile:
    data=myfile.readlines()
data = [w.replace('\n', '') for w in data]
initial_line = data.index('-------------------------')
errors = int(re.sub("[^0-9]", "", data[(initial_line - 1)]))
num_lines = len(data)
line_pos = (initial_line + 2);
new_file = []

while (data[line_pos] != "NAILS MISSING on Unused Pins:"):
    if (data[line_pos].count(':') != 1):
        while (data[line_pos] != ""):
            new_file.append(data[line_pos])
            line_pos += 1
        new_file.append("")
    else:
        errors = errors - 1
        while (data[line_pos] != ""):
            line_pos += 1
    line_pos += 1

for x in range(line_pos, num_lines):
    new_file.append(data[x])

top_stuff = str(data[0]) + "\r\n\r\n"
new_file.insert(0, top_stuff + "NAILS MISSING on " + str(errors) + " Nets:\r\n-------------------------\r\n\r\n")
file = open("OUTPUTS\Cust_Status.asc", "w")

for x in new_file:
    file.write(x + "\r\n")
    
myfile.close()
file.close()
