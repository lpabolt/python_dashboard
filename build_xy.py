import sys
import xlrd
import os
from csv import reader
import string

version_num = int(sys.argv[1])

delimiter_possibles = [' ',';']
grouping_possibles = ['-','/']
column_letters_to_numbers = {"A":0, "B":1, "C":2, "D":3, "E":4, "F":5, "G":6, "H":7, "I":8, "J":9, "K":10, "L":11, "M":12, \
                                 "N":13, "O":14, "P":15, "Q":16, "R":17, "S":18, "T":19, "U":20, "V":21, "W":22, "X":23, "Y":24, "Z":25}

with open ("OUTPUTS\Parts.asc", "r") as myfile:
    data_file=myfile.readlines()

data_file = [w.replace('\n', '') for w in data_file]

not_in_parts = []
description_arr = []
initial_loop = 0
version_name = 2
component_name = 3
part_name = 4
description_col = 5
data_starts = 6
while initial_loop < version_num:
    csv_split = []
    with open ("OUTPUTS/" + sys.argv[(len(sys.argv) - version_num) + initial_loop], "r") as myfile2:
        data_file2=myfile2.readlines()
    data_file2 = [w.replace('\n', '') for w in data_file2]
    for index,stuff in enumerate(reader(data_file2)):
        if index >= int(sys.argv[data_starts]) - 1:
            data_str = stuff[column_letters_to_numbers[sys.argv[component_name]]]
            for delims in delimiter_possibles:
                data_str = str.replace(data_str, delims, ",")
            if data_str != "":
                csv_split.append(data_str)
    for everything in csv_split:
        holder = everything.split(",")
        for indexer,find_in_data in enumerate(holder):
            if find_in_data != "":
                if find_in_data not in data_file:
                    not_in_parts.append(find_in_data +  " <<< " + str(sys.argv[version_name]))
    data_file2 = ""
    data_starts += 5
    version_name += 5
    component_name += 5
    part_name += 5
    description_col += 5
    initial_loop += 1

if len(not_in_parts) > 0:
    file = open ("OUTPUTS\components_in_BOM_but_not_parts_file.txt", "w")
    not_in_parts = list(set(not_in_parts))
    for everything in not_in_parts:
        file.write(str(everything) + '\n')
else:
    final_loop = 0

    cad_xy = {}

    ##  these are the relative positions of these in sys.argv
    ##  just add 4 to them each iteration
    version_name = 2
    component_name = 3
    part_name = 4
    description_col = 5
    data_starts = 6
    title_arr = []
    descrip_sanity = []

    descriptions_file = open ("OUTPUTS\descriptions.csv", "w")
    while final_loop < version_num:
        component_column = []
        part_column = []
    ##    book = xlrd.open_workbook("version" + str((final_loop + 1)) + ".csv")
    ##    title_arr.append(str(sys.argv[version_name]))
    ##    sheet = book.sheets()[0]
    ##    component_column = sheet.col_values(column_letters_to_numbers[sys.argv[component_name]])
    ##    part_column = sheet.col_values(column_letters_to_numbers[sys.argv[part_name]])
        title_arr.append(str(sys.argv[version_name]))
        with open ("OUTPUTS/" + sys.argv[(len(sys.argv) - version_num) + final_loop], "r") as myfile2:
            data_file2=myfile2.readlines()
        data_file2 = [w.replace('\n', '') for w in data_file2]
        for index,everything in enumerate(reader(data_file2)):
            if index >= int(sys.argv[data_starts]) - 1:
                data_str = everything[column_letters_to_numbers[sys.argv[component_name]]]
                part_num = everything[column_letters_to_numbers[sys.argv[part_name]]]
                if part_num not in descrip_sanity:
                    write_to_descrip = everything[column_letters_to_numbers[sys.argv[description_col]]]
                    write_to_descrip = write_to_descrip.replace(",",".")
                    descriptions_file.write(str(part_num) + ",\"" + str(write_to_descrip) + "\"\n")
                    descrip_sanity.append(part_num)
                for delims in delimiter_possibles:
                    data_str = str.replace(data_str, delims, ",")
                data_str = data_str.split(",")
                for each in data_str:
                    if each != "":
                        component_column.append(each)
                        part_column.append(part_num)
        part_column_copy = []
        component_column_copy = []
        for all_things_1 in part_column:
            part_column_copy.append(all_things_1)
        for all_things_2 in component_column:
            component_column_copy.append(all_things_2)
        for everything in data_file:
            if everything in component_column_copy:
                get_index = component_column_copy.index(everything)
                component_column_copy[get_index] = "$$$$"
                if final_loop == 0:
                    cad_xy.update({everything: [part_column_copy[get_index]]})
                else:
                    if everything in cad_xy.keys():
                        cad_xy[everything].append(part_column_copy[get_index])
                    else:
                        cad_xy.update({everything: [part_column_copy[get_index]]})
            else:
                if final_loop == 0:
                    cad_xy.update({everything: ["NOT_FITTED"]})
                else:
                    cad_xy[everything].append("NOT_FITTED")
        version_name += 5
        component_name += 5
        part_name += 5
        data_starts += 5
        description_col += 5
        final_loop += 1

    descriptions_file.close()

    version_keys = []
    for everything in cad_xy.keys():
        version_keys.append(everything)
    version_keys.sort()

    file = open ("OUTPUTS/version_report.txt", "w")
    file.write(",BASE")
    for everything in title_arr:
        file.write("," + str(everything))
    file.write("\n\n")
    for everything in version_keys:
        file.write("," + str(everything) + "," + str(",".join(cad_xy[everything])) + "\n")
    file.close()

    with open ("OUTPUTS/version_report.txt", "r") as myfile:
        data_file=myfile.readlines()

    ## analyse rows to find the amount of commas (fields)

    ## first column is the master file and all other files are children of that
    ## if component is fitted on the first column get rid of the first column. 
    ##      if it's got the same number on subsequent columns get rid of them
    ##      as well
    ## if it's not fitted on one then still give all columns

    data_file = [w.replace('\n', '') for w in data_file]
    data_arr = []
    title_remove = data_file[0]
    if (title_remove[0] == ","):
        title_remove = title_remove[1:]
    if (title_remove[-1] == ","):
        title_remove = title_remove[:-1]
    breakdown_titles = title_remove.split(",")
    breakdown_titles.pop(0)

    for x in data_file:
        if (x != ""):
            line = x
            if (line[0] == ","):
                line = line[1:]
            if (line[-1] == ","):
                line = line[:-1]
            data_arr.append(line)
        else:
            data_arr.append("\n")
    file_list = []
    not_fitted_file_list = []
    initial_not_fitted = 0
    column_problems = 0
    column_errs = []

    get_columns = len(data_arr[0].split(",",100))
    for x in data_arr:
        if (x != data_arr[1]):
            holder = []
            holder.append(x.split(",",100))
            if (len(holder[0]) < get_columns):
                column_problems += 1
                column_errs.append(holder[0])

    if (column_problems > 0):
        file = open("OUTPUTS/version_report_errors.txt", "w")
        file.write(str(data_arr[0]) + "\n\n*****************THE FOLLOWING ROWS WERE WRONG*****************\n\n")

        for x in column_errs:
            new_line = ','.join(x)
            file.write(new_line + "\r\n")
    else:
        for x in data_arr:
            if (x != data_arr[1]):
                holder = []
                holder.append(x.split(",",100))
                if (holder[0] == ""):
                    file_list.append("")
                else:
                    if (holder[0][1] != "NOT_FITTED"):
                        file_list.append(holder[0])
                    else:
                        not_fitted_file_list.append(holder[0])
                    list_len = len(holder[0])
                        

        file = open("OUTPUTS/version_report_split.txt", "w")
        file.write(str(data_file[0]) + "\n\n")
        file_list.pop(0)

        varies = []
        file.write("\nALL FITTED\n\n")
        for x in file_list:
            new_line = ','.join(x)
            if len(set(x)) > 2:
                varies.append(new_line)
            else:
                file.write(new_line + "\n")

        if len(varies) > 0:
            file.write("\nVARIABLE\n\n")
            for all_them in varies:
                file.write(all_them + "\n")

        file.write("\nALL NOT FITTED\n\n")
        columns = list_len - 1

        for y in not_fitted_file_list:
            if y.count("NOT_FITTED") == columns:
                new_line = ','.join(y)
                file.write(new_line + "\n")

        file.write("\nINITIAL NOT FITTED\n\n")

        for z in not_fitted_file_list:
            if z.count("NOT_FITTED") < columns:
                new_line = ','.join(z)
                file.write(new_line + "\n")

        file.close()

        ############# BREAKDOWN PART #############

    ##    THIS PART BELOW PUTS EVERYTHING ON SEPARATE LINES IN THE ONE FILE
    ## *******************************************************************
        with open ("OUTPUTS/version_report_split.txt", "r") as myfile:
            data_file=myfile.readlines()
        data_file = [w.replace('\n', '') for w in data_file]
        data_file.pop(0)
        data_file.pop(0)
        version_arr = []
        final_arr = []

        file = open("OUTPUTS/version_report_breakdown.txt", "w")
        file.write("COMPONENT,VERSION,NOTES\n\n")
        
        data_file.pop(0)
        data_file.pop(0)
        version_arr = []
        final_arr = []

        for lines in data_file:
            if (lines != ""):
                if (lines != "ALL NOT FITTED" and lines != "INITIAL NOT FITTED" and lines != "VARIABLE" and lines != "ALL FITTED"):
                    version_arr.append(lines.split(","))
        changes_in_versions = []
        pop_arr = []
        for index, finals in enumerate(version_arr):
            not_not_fitted = []
            not_not_fitted_code = []
            if finals.count("NOT_FITTED") == len(title_arr):
                for everything in title_arr:
                    file.write(str(finals[0]) + "," + str(everything) + ",NOT_FITTED\n")
            else:
                if finals[1] == "NOT_FITTED":
                    notes_str = " in version "
                    notes_versions = []
                    notes_part = []
                    notes_part_dupes = []
                    notes_versions_inc = 0
                    for nums, inner in enumerate(finals):
                        if nums > 0:
                            if inner != "NOT_FITTED":
                                file.write(str(finals[0]) + "," + str(title_arr[nums - 1]) + ",NOT_FITTED\n")
##                    dupe_parts = list(set(notes_part_dupes))
##                    if len(dupe_parts) == 1:
##                        for everything in notes_part:
##                            file.write(str(finals[0]) + "," + str(title_arr[nums]) + ",NOT_FITTED   <<< " + str(dupe_parts[0]) + " in version(s) " + str(",".join(notes_versions)) + "\n")
##                    else:
##                        if len(dupe_parts) > 1:
##                            for everything in notes_part:
##                                file.write(str(finals[0]) + "," + str(title_arr[nums]) + ",NOT_FITTED   <<< MULTIPLE PART NUMBERS in version(s) " + str(",".join(notes_versions)) + "\n")
                else:
                    for nums, inner in enumerate(finals):
                        if nums > 1:
                            if inner != finals[1]:
                                file.write(str(finals[0]) + "," + str(title_arr[nums - 1]) + "," + str(inner) + "\n")
    ##              YOU'VE GOT TO DO THE BIT WHERE IT LOOKS FOR DIFFERENCES TO THE INITIAL NOT_FITTED.
        file.close()
        
        with open ("OUTPUTS/version_report_breakdown.txt", "r") as myfile:
            data_file=myfile.readlines()
        myfile.close()
        data_file = [w.replace('\n', '') for w in data_file]
        file = open("OUTPUTS/version_report_breakdown.txt", "w")
        data_file.sort()
        file.write("COMPONENT,VERSION,NOTES\n")
        for everything in data_file:
            file.write(str(everything) + "\n")






        
##        for a in range(0,len(finals)):
##            if a != 0:
##                if finals[a] != "NOT_FITTED" and finals[a] != main_check:
##                    not_not_fitted.append(a)
##                    not_not_fitted_code.append(finals[a])
##        not_not_fitted_code = list(set(not_not_fitted_code))
##        length = int(len(finals)) - 1
##        inc = 0
##        not_fitted_count = length - 1
##        while inc < length:
##            
##            if finals[inc + 1] == "NOT_FITTED":
##                if len(not_not_fitted) > 0:
##                    add_to_string = str(";".join(str(x) for x in not_not_fitted))
##                    if len(not_not_fitted_code) > 0:
##                        if len(not_not_fitted_code) == 1:
##                            versions_string = ""
##                            for versions in not_not_fitted:
##                                versions_string += str(breakdown_titles[versions - 1]) + "; "
##                            final_arr.append(str(finals[0]) + "," + str(breakdown_titles[inc]) + ",NOT_FITTED   <<< " + str(not_not_fitted_code[0]) \
##                                       + " in version " + str(versions_string) + "\n")
##                        else:
##                            versions_string = ""
##                            for versions in not_not_fitted:
##                                versions_string += str(breakdown_titles[versions - 1]) + "; "
##                            final_arr.append(str(finals[0]) + "," + str(breakdown_titles[inc]) + ",NOT_FITTED   <<< MULTIPLE PART NUMBERS in version " \
##                                       + str(versions_string) + "\n")
##                    else:
##                        final_arr.append(str(finals[0]) + "," + str(breakdown_titles[inc]) + ",NOT_FITTED\n")
##                else:
##                    final_arr.append(str(finals[0]) + "," + str(breakdown_titles[inc]) + ",NOT_FITTED\n")
##            else:
##                if finals[inc + 1] != "NOT_FITTED" and finals[inc + 1] != main_check:
##                    final_arr.append(str(finals[0]) + "," + str(breakdown_titles[inc]) + "," + str(finals[inc + 1]) + "\n")
##            inc += 1

                
##    final_arr.sort()
##    file = open("cad_xy_breakdown.txt", "w")
##    file.write("COMPONENT,VERSION,NOTES\n\n")
##    for everything in final_arr:
##        file.write(everything)
            
## *******************************************************************


##  THIS IS THE DESCRIPTION BIT FOR THE CSV FILE FOR JIM/PAUL AND THAT.
##  YOU'LL NEED TO ADD IN THE FIELD TO GET THE COLUMN LOCATION OF DESCRIPTION IN index.php

## IT'S IN G IN THESE FILES
desc_column = 6
desc_dict = {}

with open ("OUTPUTS/descriptions.csv", "r") as myfile:
    descrip = myfile.readlines()
descrip = [w.replace('\n', '') for w in descrip]

for everything in reader(descrip):
    desc_dict.update({everything[0]: str(everything[1])})

with open ("OUTPUTS/version_report.txt", "r") as myfile:
    data_file = myfile.readlines()
data_file = [w.replace('\n', '') for w in data_file]

file = open("OUTPUTS/version_breakdown_spreadsheet.csv", "w")
file.write(str("ALL DEVICES,"))
##  GET FROM breakdown_titles ABOVE
for all_things in title_arr:
    file.write("," + str(all_things))
file.write(str("\n"))

for nums,everything in enumerate(data_file):
    if nums > 1:
        holder = everything.split(",")
        holder.pop(0)
        new_var = everything.split(",")
        new_var.pop(0)
        new_var.pop(0)
        check_list = list(set(new_var))
        if len(check_list) == 1:
            if "NOT_FITTED" in check_list:
                file.write(str(holder[0]) + ',NF,\n')
            else:
                file.write(str(holder[0]) + ',' + str(desc_dict[new_var[1]]) + ',\n')
        else:
            for cols,things in enumerate(holder):
                if cols == 0:
                    file.write(str(things) + ',***')
                else:
                    if cols > 0:
                        if things != "NOT_FITTED":
                            file.write(',' + str(desc_dict[things]))
                        else:
                            file.write(',NF')
            file.write(str('\n'))
