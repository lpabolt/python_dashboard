import os

with open ("cad_xy.txt", "r") as myfile:
    data_file=myfile.readlines()

## analyse rows to find the amount of commas (fields)

## first column is the master file and all other files are children of that
## if component is fitted on the first column get rid of the first column. 
##      if it's got the same number on subsequent columns get rid of them
##      as well
## if it's not fitted on one then still give all columns

data_file = [w.replace('\r\n', '') for w in data_file]
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
        data_arr.append("\r\n")
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
    file = open("cad_xy_errors.txt", "w")
    file.write(str(data_arr[0]) + "\r\n\r\n*****************THE FOLLOWING ROWS WERE WRONG*****************\r\n\r\n")

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
                    

    file = open("cad_xy_edited.txt", "w")
    file.write(str(data_file[0]) + "\r\n\r\n")
    file_list.pop(0)

    for x in file_list:
        new_line = ','.join(x)
        file.write(new_line + "\r\n")

    file.write("\r\nALL NOT FITTED\r\n\r\n")
    columns = list_len - 1

    for y in not_fitted_file_list:
        if y.count("NOT_FITTED") == columns:
            new_line = ','.join(y)
            file.write(new_line + "\r\n")

    file.write("\r\nINITIAL NOT FITTED\r\n\r\n")

    for z in not_fitted_file_list:
        if z.count("NOT_FITTED") < columns:
            new_line = ','.join(z)
            file.write(new_line + "\r\n")

    file.close()

    ############# BREAKDOWN PART #############

##    THIS PART BELOW SPLITS EVERYTHING INTO SEPARATE .CSV FILES
## *******************************************************************
    version_arr = []
    for u in range(0,(get_columns - 1)):
        file = open("version_" + str(u + 1) + ".csv", "w+")
        file.close()
        version_arr.append("version_" + str(u + 1) + ".csv")

    with open ("cad_xy_edited.txt", "r") as myfile:
        data_file=myfile.readlines()
    data_file = [w.replace('\r\n', '') for w in data_file]
    
    data_file.pop(0)
    data_file.pop(0)
    version_arr = []
    final_arr = []

    for lines in data_file:
        if (lines != ""):
            if (lines != "ALL NOT FITTED" and lines != "INITIAL NOT FITTED"):
                version_arr.append(lines.split(","))

    changes_in_versions = []
    pop_arr = []
    for index, finals in enumerate(version_arr):
        not_not_fitted = []
        not_not_fitted_code = []
        main_check = finals[1]
        for a in range(0,len(finals)):
            if a != 0:
                if finals[a] != "NOT_FITTED" and finals[a] != main_check:
                    not_not_fitted.append(a)
                    not_not_fitted_code.append(finals[a])
        not_not_fitted_code = list(set(not_not_fitted_code))
        length = int(len(finals)) - 1
        inc = 0
        not_fitted_count = length - 1
        while inc < length:
            if finals[inc + 1] == "NOT_FITTED":
                file = open("version_" + str((inc + 1)) + ".csv", "a")
                if len(not_not_fitted) > 0:
                    add_to_string = str(";".join(str(x) for x in not_not_fitted))
                    if len(not_not_fitted_code) > 0:
                        if len(not_not_fitted_code) == 1:
##                            file.write(str(finals[0]) + "," + str(breakdown_titles[inc]) + ",NOT_FITTED   <<< " + str(not_not_fitted_code[0]) \
##                                       + " in version ")
                            file.write(str(finals[0]) + "," + str(breakdown_titles[inc]) + ",NOT_FITTED\n")
                            ## THE BELOW IS ACTIVE IF THE ABOVE COMMENT BECOMES ACTIVE
##                            for versions in not_not_fitted:
##                                file.write(str(breakdown_titles[versions - 1]) + "; ")
##                            file.write("\n")
                        else:
##                            file.write(str(finals[0]) + "," + str(breakdown_titles[inc]) + ",NOT_FITTED   <<< MULTIPLE PART NUMBERS in version " \
##                                       + str(add_to_string) + "\n")
                            file.write(str(finals[0]) + "," + str(breakdown_titles[inc]) + ",NOT_FITTED\n")
                    else:
                        file.write(str(finals[0]) + "," + str(breakdown_titles[inc]) + ",NOT_FITTED\n")
                else:
                    file.write(str(finals[0]) + "," + str(breakdown_titles[inc]) + ",NOT_FITTED\n")
                file.close()
            else:
                if finals[inc + 1] != "NOT_FITTED" and finals[inc + 1] != main_check:
                    file = open("version_" + str((inc + 1)) + ".csv", "a")
                    file.write(str(finals[0]) + "," + str(breakdown_titles[inc]) + "," + str(finals[inc + 1]) + "\n")
            inc += 1
## *******************************************************************

##    THIS PART BELOW PUTS EVERYTHING ON SEPARATE LINES IN THE ONE FILE
## *******************************************************************
    with open ("cad_xy_edited.txt", "r") as myfile:
        data_file=myfile.readlines()
    data_file = [w.replace('\r\n', '') for w in data_file]
    data_file.pop(0)
    data_file.pop(0)
    version_arr = []
    final_arr = []

    for lines in data_file:
        if (lines != ""):
            if (lines != "ALL NOT FITTED" and lines != "INITIAL NOT FITTED"):
                version_arr.append(lines.split(","))

    file = open("cad_xy_breakdown.txt", "w")
    
    data_file.pop(0)
    data_file.pop(0)
    version_arr = []
    final_arr = []

    for lines in data_file:
        if (lines != ""):
            if (lines != "ALL NOT FITTED" and lines != "INITIAL NOT FITTED"):
                version_arr.append(lines.split(","))

    changes_in_versions = []
    pop_arr = []
    for index, finals in enumerate(version_arr):
        not_not_fitted = []
        not_not_fitted_code = []
        main_check = finals[1]
        for a in range(0,len(finals)):
            if a != 0:
                if finals[a] != "NOT_FITTED" and finals[a] != main_check:
                    not_not_fitted.append(a)
                    not_not_fitted_code.append(finals[a])
        not_not_fitted_code = list(set(not_not_fitted_code))
        length = int(len(finals)) - 1
        inc = 0
        not_fitted_count = length - 1
        while inc < length:
            if finals[inc + 1] == "NOT_FITTED":
                if len(not_not_fitted) > 0:
                    add_to_string = str(";".join(str(x) for x in not_not_fitted))
                    if len(not_not_fitted_code) > 0:
                        if len(not_not_fitted_code) == 1:
                            versions_string = ""
                            for versions in not_not_fitted:
                                versions_string += str(breakdown_titles[versions - 1]) + "; "
                            final_arr.append(str(finals[0]) + "," + str(breakdown_titles[inc]) + ",NOT_FITTED   <<< " + str(not_not_fitted_code[0]) \
                                       + " in version " + str(versions_string) + "\r\n")
                        else:
                            versions_string = ""
                            for versions in not_not_fitted:
                                versions_string += str(breakdown_titles[versions - 1]) + "; "
                            final_arr.append(str(finals[0]) + "," + str(breakdown_titles[inc]) + ",NOT_FITTED   <<< MULTIPLE PART NUMBERS in version " \
                                       + str(versions_string) + "\r\n")
                    else:
                        final_arr.append(str(finals[0]) + "," + str(breakdown_titles[inc]) + ",NOT_FITTED\r\n")
                else:
                    final_arr.append(str(finals[0]) + "," + str(breakdown_titles[inc]) + ",NOT_FITTED\r\n")
            else:
                if finals[inc + 1] != "NOT_FITTED" and finals[inc + 1] != main_check:
                    final_arr.append(str(finals[0]) + "," + str(breakdown_titles[inc]) + "," + str(finals[inc + 1]) + "\r\n")
            inc += 1

                
    final_arr.sort()
    file = open("cad_xy_breakdown.txt", "w")
    file.write("COMPONENT,VERSION,NOTES\r\n\r\n")
    for everything in final_arr:
        file.write(everything)
            
## *******************************************************************
